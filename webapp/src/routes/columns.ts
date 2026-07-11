import type { ColumnDef } from "@tanstack/table-core";

export type Restaurant = {
  name: string;
  date: Date;
  '1 stars': number;
  '2 stars': number;
  '3 stars': number;
  '4 stars': number;
  '5 stars': number;
}

export const columns: ColumnDef<Restaurant>[] = [
 {
  accessorKey: "name",
  header: "Name",
 },
 {
  accessorKey: "date",
  header: "Date",
 },
 {
  accessorKey: "1 stars",
  header: "1 Star",
 },
 {
  accessorKey: "2 stars",
  header: "2 Star",
 },
 {
  accessorKey: "3 stars",
  header: "3 Star",
 },
 {
  accessorKey: "4 stars",
  header: "4 Star",
 },
 {
  accessorKey: "5 stars",
  header: "5 Star",
 },
];
