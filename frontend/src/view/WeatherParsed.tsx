import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {WeatherParsedItem} from "../types.ts";
import {formatDate} from "../utils.ts";

const columns: Column<WeatherParsedItem>[] = [
  { key: "parsed_at", header: "Дата загрузки", render: (i) => formatDate(i.parsed_at)},
  { key: "observed_date", header: "Дата", render: (i) => formatDate(i.observed_date, "date")},
  { key: "precipitation", header: "Осадки, мм", render: (i) => i.precipitation},
  { key: "temp_min", header: "Минимальная температура", render: (i) => i.temp_min},
  { key: "temp_mean", header: "Средняя температура", render: (i) => i.temp_mean},
  { key: "temp_max", header: "Максимальная температура", render: (i) => i.temp_max},
  { key: "temp_dev", header: "Отклонение температуры", render: (i) => i.temp_dev},
];

export const WeatherParsed = () => {
  const weather = useList<WeatherParsedItem>({ url: "/api/weather_parsed" });

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