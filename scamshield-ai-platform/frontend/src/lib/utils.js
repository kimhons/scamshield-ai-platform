import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export function formatDate(date) {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(date))
}

export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount)
}

export function generateId() {
  return Math.random().toString(36).substr(2, 9)
}

export function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export function truncateText(text, maxLength = 100) {
  if (text.length <= maxLength) return text
  return text.substr(0, maxLength) + '...'
}