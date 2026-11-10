import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {WeatherCleanItem} from "../types.ts";
import {formatDate} from "../utils.ts";

const columns: Column<WeatherCleanItem>[] = [
  { key: "created_at", header: "Дата обработки", render: (i) => formatDate(i.created_at)},
  { key: "observed_date", header: "Дата", render: (i) => formatDate(i.observed_date, 'date')},
  { key: "temp_mean_lag_1", header: "T_mean лаг 1", render: (i) => i.temp_mean_lag_1},
  { key: "temp_mean_mean_3", header: "T_mean среднее 3", render: (i) => i.temp_mean_mean_3},
  { key: "temp_mean_mean_7", header: "T_mean среднее 7", render: (i) => i.temp_mean_mean_7},
  { key: "temp_min_lag_1", header: "T_min лаг 1", render: (i) => i.temp_min_lag_1},
  { key: "temp_min_min_3", header: "T_min мин 3", render: (i) => i.temp_min_min_3},
  { key: "temp_max_lag_1", header: "T_max лаг 1", render: (i) => i.temp_max_lag_1},
  { key: "temp_change", header: "Изменение T_mean", render: (i) => i.temp_change},
  { key: "temp_dev_lag_1", header: "Отклонение T_mean лаг 1", render: (i) => i.temp_dev_lag_1},
  { key: "precipitation_lag_1", header: "Осадки лаг 1", render: (i) => i.precipitation_lag_1},
  { key: "precipitation_sum_3", header: "Осадки сумма 3", render: (i) => i.precipitation_sum_3},
  { key: "precipitation_sum_7", header: "Осадки сумма 7", render: (i) => i.precipitation_sum_7},
];

export const WeatherClean = () => {
  const weather = useList<WeatherCleanItem>({ url: "/api/weather" });

  return (
    <List
      items={weather.items}
      total={weather.total}
      columns={columns}
      loading={weather.loading}
      emptyText="Нет данных"
      pager={{
        page: weather.page,
        pages: weather.pages ?? 0,
        onChange: weather.setPage,
      }}
      getKey={(i) => i.station_id + " " + i.observed_date}
    />
  );
};