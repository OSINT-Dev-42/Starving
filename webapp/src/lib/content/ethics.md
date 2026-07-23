# Legal and ethical handling of the project Starving

This is a write-up of legal and ethical concerns for our project and how we handle them.
In general, this should be both a little checklist to follow as well as our answers to the points on that list.

## Legal (non) Compliance

A list of legal concerns that have to be addressed in some way or another.

- Jurisdiction Compliance
- Terms of Service
- Intellectual Property/ Licensing/ Copyright

### Legal Compliance:

We are located in Germany, so we have to consider the GDPR and the DSGVO in the handling of our data. We scraped only public comments (ratings) and no data connected in any way to specific persons, so these laws do not apply to us.

### Terms of Service

We scrape Google Maps and break their ToS. In our scraping, we don't use accounts and avoid IP bans by routing our traffic over Tor.
Still we adhere to the politeness policy to ensure we do not perform a Denial of Service attack on Google's infrastructure, we maintain a low request frequency.

### Intellectual Property

Facts like a numerical star rating are generally not subject to copyright. However, the database itself might be protected under the Sui Generis Database Right. We are not redistributing the database. We are generating transformative research results.

## Human Rights & Humanitarian Ethics

- Physical Safety: Does our research put individuals at risk of retaliation, arrest, or physical violence?
- How do we ensure privacy if necessary?
- Does the exposure of this information cause harm to unrelated third parties?
- No harm to researchers
- Public vs. private data: truly public data intended to be seen vs. publicly available (e.g., private profiles)

### Harm Mitigation

Our research focuses on business entities, not individuals. However, if our research publicly calls out a business for "tampering", that business might face economic loss.

## Operational concerns

- Have we employed hashing to ensure our collected data hasn't been altered after download?
- Metadata (non) preservation
- Archiving

### Hashing

We did not apply hashing to our data collection, as we did not think it necessary for our project.

### Metadata

We do not preserve any metadata from our crawls. The data we collect doesn't need scrubbing of metadata.

### Archiving

We use git to archive the data collected.

## Scientific/ Academic Ethics

- Methodological Transparency
- Bias Mitigation

### Methodological Transparency

We publish our methodology on our website presenting the results

### Bias Mitigation

Google's internal algorithms create a skewed view. This means the data we provide do not represent an objective truth, but a view curated by Google. Also, a dip in ratings is first and foremost a correlation.

## Sources

- https://obsint.eu/wp-content/uploads/2023/04/Guidelines-for-Open-Source-Intelligence-Organisations.pdf
- https://www.ohchr.org/sites/default/files/2024-01/OHCHR_BerkeleyProtocol.pdf
- https://shadowdragon.io/wp-content/uploads/2026/02/OSINT-Checklist.pdf
