type DatePreset = "datetime" | "date" | "time" | "short";

const PRESETS: Record<DatePreset, Intl.DateTimeFormatOptions> = {
  datetime: { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" },
  date: { year: "numeric", month: "2-digit", day: "2-digit" },
  time: { hour: "2-digit", minute: "2-digit" },
  short: { day: "numeric", month: "short" },
};

export const formatDate = (
  value: string | null | undefined,
  format: DatePreset | Intl.DateTimeFormatOptions = "datetime",
  locale = "ru-RU",
): string => {
  if (!value) return "—";

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";

  const options = typeof format === "string" ? PRESETS[format] : format;
  return date.toLocaleString(locale, options);
};