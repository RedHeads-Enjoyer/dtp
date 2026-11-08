export type DtpItem = {
  id: number;
  tags: string;
  category: string;
  region: string;
  county: string;
  address: string;
  longitude: number;
  latitude: number;
  nearby: string;
  datetime: string;
  light: string;
  weather: string;
  road_conditions: string;
  participants_count: number;
  participant_categories: string;
  severity: string;
  dead_count: number;
  injured_count: number;
};

export type LoadLogItem = {
  id: number;
  file_name: string;
  started_at: string;
  finished_at: string;
  status: "ok" | "empty" | "error" | string;
  rows_total: number;
  rows_inserted: number;
  error: string | null;
};

export type RawWeatherItem = {
  id: number;
  requested_at: string;
  responded_at: string;
  url: string;
  html: string | null;
  error: string | null;
};

export type WeatherItem = {
  id: number;
  observed_date: string;
  parsed_at: string;
  precipitation: number;
  raw_id: number;
  station_id: number;
  temp_dev: number;
  temp_max: number;
  temp_mean: number;
  temp_min: number;
};

export type Page<T> = {
  items: T[];
  total: number;
  page?: number;
  pages?: number;
};