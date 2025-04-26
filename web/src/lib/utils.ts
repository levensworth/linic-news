import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getFormattedDate(dateString: string): string {
  const date = new Date(dateString);
  return `${date.getDate()} / ${date.getMonth() + 1} / ${date.getFullYear()}`;
}