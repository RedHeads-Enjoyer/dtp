import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {RawWeatherItem} from "../types.ts";
import {formatDate} from "../utils.ts";
import {Loader} from "../components/Loader/Loader.tsx";

const columns: Column<RawWeatherItem>[] = [
  { key: "id", header: "Номер", render: (i) => i.id },
  { key: "requested_at", header: "Дата постановки в очередь", render: (i) => formatDate(i.requested_at)},
  { key: "responded_at", header: "Дата загрузки", render: (i) => formatDate(i.responded_at)},
  { key: "url", header: "Запрос", render: (i) => i.url},
  {
    key: "html",
    header: "Ответ",
    render: (i) => i.error || i.html
      ? i.html
      : <Loader />,
    className: "ellipsis"
  },
  {
    key: "error",
    header: "Ошибка",
    render: (i) =>  i.error ?? "—",
    className: "ellipsis"
  },
];

export const RawWeather = () => {
  const weather = useList<RawWeatherItem>({ url: "/api/raw_weather" });

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
    />
  );
};