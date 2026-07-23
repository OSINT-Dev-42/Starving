import pandas as pd
import pathlib as path
import json
import re
import unicodedata
from datetime import date


PATH = path.Path(__file__).parents[2]

CSV_PATH = PATH / 'data' / 'raw' / 'firstcrawl.csv'
OUT_PATH = PATH / 'webapp' / 'src' / 'lib' / 'data' / 'summary.json'
LIST_PATH = PATH / 'webapp' / 'src' / 'lib' / 'data' / 'restaurants.json'
DETAIL_PATH = PATH / 'webapp' / 'src' / 'lib' / 'data' / 'restaurant-details.json'

# the restaurant featured in the hero chart (matched by name prefix, because
# the name changed mid-crawl e.g. "Trattoria Momo, Bochum Stadionring 9")
FEATURED = 'Trattoria Momo'


df = pd.read_csv(CSV_PATH)
df = df[df.name != '>>>>>>> Stashed changes']

star_cols = ['5 stars', '4 stars', '3 stars', '2 stars', '1 stars']
for col in star_cols:
    df[col] = df[col].astype(str).str.replace(',', '').astype(float).astype(int)

df['date'] = pd.to_datetime(df['date'], format='mixed')
df['day'] = df['date'].dt.date

# group by the name before the first comma, so a restaurant that was renamed
# mid-crawl (Trattoria Momo) does not show up twice
df['base'] = df['name'].str.split(',').str[0].str.strip()

# drop failed scrapes: sometimes a star count is stored as the star number
# itself, e.g. "5 stars" reads 5 where the previous scrape read 1047.
# make_graphs.py skips the same pattern in find_anomalies.
df = df.sort_values('date')
star_numbers = {'5 stars': 5, '4 stars': 4, '3 stars': 3, '2 stars': 2, '1 stars': 1}
glitched = pd.Series(False, index=df.index)
for col, num in star_numbers.items():
    previous = df.groupby('base')[col].shift()
    glitched |= (df[col] == num) & (previous > 10 * num)
print(f"dropping {int(glitched.sum())} failed scrapes")
df = df[~glitched]


featured_df = df[df['name'].str.startswith(FEATURED)]
featured_df = featured_df.sort_values('date')
featured_df = featured_df.drop_duplicates(subset=['day'], keep='last')

series = []
for _, row in featured_df.iterrows():
    series.append({
        'date': row['day'].isoformat(),
        's5': int(row['5 stars']),
        's4': int(row['4 stars']),
        's3': int(row['3 stars']),
        's2': int(row['2 stars']),
        's1': int(row['1 stars']),
    })

## latest snapshot for the featured restaurant (table view)
last = featured_df.iloc[-1]
total = int(last['5 stars'] + last['4 stars'] + last['3 stars'] + last['2 stars'] + last['1 stars'])
weighted = (5 * last['5 stars'] + 4 * last['4 stars'] + 3 * last['3 stars']
            + 2 * last['2 stars'] + 1 * last['1 stars'])
average = round(weighted / total, 2) if total else 0
notice = last['notice'] if isinstance(last['notice'], str) else ''

latest = {
    's5': int(last['5 stars']),
    's4': int(last['4 stars']),
    's3': int(last['3 stars']),
    's2': int(last['2 stars']),
    's1': int(last['1 stars']),
    'total': total,
    'average': average,
    'notice': notice,
}


deltas = []
for name in df['name'].unique():
    r_df = df[df['name'] == name].sort_values('date').drop_duplicates(subset=['day'], keep='last')
    for col in star_cols:
        values = r_df[col].tolist()
        days = r_df['day'].tolist()
        diffs = [values[i] - values[i - 1] for i in range(1, len(values))]
        for i, delta in enumerate(diffs):
            if delta == 0:
                continue
            # drop this step if it is (mostly) cancelled by the next or previous
            # step -> it is one leg of a transient spike/glitch
            nxt = diffs[i + 1] if i + 1 < len(diffs) else 0
            prev = diffs[i - 1] if i - 1 >= 0 else 0
            if abs(delta + nxt) < 0.5 * abs(delta) or abs(delta + prev) < 0.5 * abs(delta):
                continue
            deltas.append({
                'name': name,
                'stars': col,
                'delta': int(delta),
                'date': days[i + 1].isoformat(),
            })

# keep the 5 biggest increases and 5 biggest deletions
deltas.sort(key=lambda d: d['delta'], reverse=True)
largest_deltas = deltas[:5] + deltas[-5:]


summary = {
    'generatedAt': date.today().isoformat(),
    'featured': {
        'name': last['name'],
        'series': series,
        'latest': latest,
    },
    'largestDeltas': largest_deltas,
}

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
print(f"wrote {OUT_PATH} ({len(series)} featured points, {len(largest_deltas)} deltas)")


## per restaurant list + details for the webapp tables
def slugify(name):
    ascii_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', ascii_name.lower())).strip('-')


restaurant_list = []
restaurant_details = {}

for base_name in df['base'].unique():
    r_df = df[df['base'] == base_name].sort_values('date')
    r_df = r_df.drop_duplicates(subset=['day'], keep='last')

    rows = []
    for _, row in r_df.iterrows():
        row_total = int(row['5 stars'] + row['4 stars'] + row['3 stars']
                        + row['2 stars'] + row['1 stars'])
        rows.append({
            'date': row['day'].isoformat(),
            's5': int(row['5 stars']),
            's4': int(row['4 stars']),
            's3': int(row['3 stars']),
            's2': int(row['2 stars']),
            's1': int(row['1 stars']),
            'total': row_total,
        })

    r_last = r_df.iloc[-1]
    r_total = rows[-1]['total']
    r_weighted = (5 * r_last['5 stars'] + 4 * r_last['4 stars'] + 3 * r_last['3 stars']
                  + 2 * r_last['2 stars'] + 1 * r_last['1 stars'])

    # the most recent day on which any star count moved
    last_change = None
    for i in range(len(rows) - 1, 0, -1):
        changes = []
        for key, col in zip(['s5', 's4', 's3', 's2', 's1'], star_cols):
            delta = rows[i][key] - rows[i - 1][key]
            if delta != 0:
                changes.append({'stars': col, 'delta': delta})
        if changes:
            last_change = {'date': rows[i]['date'], 'changes': changes}
            break

    # the address is whatever follows the name in the most recent full name
    full_name = r_last['name']
    address = full_name.split(',', 1)[1].strip() if ',' in full_name else ''
    slug = slugify(base_name)

    restaurant_list.append({
        'name': base_name,
        'address': address,
        'slug': slug,
        'latest': {
            's5': int(r_last['5 stars']),
            's4': int(r_last['4 stars']),
            's3': int(r_last['3 stars']),
            's2': int(r_last['2 stars']),
            's1': int(r_last['1 stars']),
            'total': r_total,
            'average': round(r_weighted / r_total, 2) if r_total else 0,
            'notice': r_last['notice'] if isinstance(r_last['notice'], str) else '',
        },
        'lastChange': last_change,
        'spark': [r['total'] for r in rows],
    })
    restaurant_details[slug] = rows

# best rated first, so the homepage can just take the first 20. review count and
# name break ties, so the order stays stable between runs
restaurant_list.sort(key=lambda r: (-r['latest']['average'], -r['latest']['total'], r['name']))

LIST_PATH.write_text(json.dumps(restaurant_list, ensure_ascii=False, indent=2))
DETAIL_PATH.write_text(json.dumps(restaurant_details, ensure_ascii=False))
print(f"wrote {LIST_PATH} ({len(restaurant_list)} restaurants)")
print(f"wrote {DETAIL_PATH}")
