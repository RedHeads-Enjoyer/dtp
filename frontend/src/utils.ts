export const formatDate = (value: string) => {
  if (!value) return("—")
  return new Date(value).toLocaleString("ru-RU");
}
