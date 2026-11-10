import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {WeatherRawItem} from "../types.ts";
import {formatDate} from "../utils.ts";
import {Loader} from "../components/Loader/Loader.tsx";

const columns: Column<WeatherRawItem>[] = [
  { key: "requested_at", header: "Дата постановки в очередь", render: (i) => formatDate(i.requested_at)},
  { key: "responded_at", header: "Дата загрузки", render: (i) => formatDate(i.responded_at)},
  { key: "url", header: "Запрос", render: (i) => i.url},
  {
    key: "html",
    header: "Ответ",
    render: (i) => i.fetch_error || i.html
      ? i.html
      : <Loader />,
    className: "ellipsis"
  },
  {
    key: "fetch_error",
    header: "Ошибка запроса",
    render: (i) =>  i.fetch_error ?? "—",
    className: "ellipsis"
  },
  {
    key: "parse_error",
    header: "Ошибка парсинга",
    render: (i) =>  i.parse_error ?? "—",
    className: "ellipsis"
  },
];

export const WeatherRaw = () => {
  const weather = useList<WeatherRawItem>({ url: "/api/weather_raw" });

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
      getKey={(i) => i.url}
    />
  );
};