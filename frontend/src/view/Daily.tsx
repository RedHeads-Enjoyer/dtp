import { formatDate } from "../utils.ts";
import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {DailyItem} from "../types.ts";

const columns: Column<DailyItem>[] = [
  { key: "id", header: "Номер", render: (i) => i.id },
  { key: "created_at", header: "Дата обработки", render: (i) => formatDate(i.created_at) },
  { key: "date", header: "Дата", render: (i) => formatDate(i.date) },
  { key: "accidents_lag_1", header: "Лаг 1", render: (i) => i.accidents_lag_1 },
  { key: "accidents_lag_7", header: "Лаг 7", render: (i) => i.accidents_lag_7 },
  { key: "accidents_roll_7", header: "Среднее 7", render: (i) => i.accidents_roll_7 },
  { key: "dow", header: "День недели", render: (i) => i.dow },
  { key: "month", header: "Месяц", render: (i) => i.month },
];

export const Daily = () => {
  const daily = useList<DailyItem>({ url: "/api/daily", pageSize: 500 });

  return (
    <List
      items={daily.items}
      total={daily.total}
      columns={columns}
      loading={daily.loading}
      emptyText="Нет данных"
      pager={{
        page: daily.page,
        pages: daily.pages ?? 0,
        onChange: daily.setPage,
      }}
      getKey={(i) => i.id}
    />
  );
};