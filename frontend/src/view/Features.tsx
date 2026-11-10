import { formatDate } from "../utils.ts";
import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {FeatureItem} from "../types.ts";

const columns: Column<FeatureItem>[] = [
  { key: "date", header: "Дата", render: (i) => formatDate(i.date, "date") },
  { key: "version", header: "Версия", render: (i) => i.version },
  { key: "accidents", header: "Количество ДТП", render: (i) => i.accidents },
  { key: "lag_1", header: "Лаг 1", render: (i) => i.lag_1 },
  { key: "lag_7", header: "Лаг 7", render: (i) => i.lag_7 },
  { key: "roll_7", header: "Среднее 7", render: (i) => i.roll_7 },
  { key: "dow", header: "День недели", render: (i) => i.dow },
  { key: "month", header: "Месяц", render: (i) => i.month },
  { key: "temp_min", header: "Минимальная температура", render: (i) => i.temp_min},
  { key: "temp_mean", header: "Средняя температура", render: (i) => i.temp_mean},
  { key: "temp_max", header: "Максимальная температура", render: (i) => i.temp_max},
  { key: "temp_dev", header: "Отклонение температуры", render: (i) => i.temp_dev},
    { key: "precipitation", header: "Осадки, мм", render: (i) => i.precipitation},
];

export const Features = () => {
  const features = useList<FeatureItem>({ url: "/api/features", pageSize: 500 });

  return (
    <List
      items={features.items}
      total={features.total}
      columns={columns}
      loading={features.loading}
      emptyText="Нет данных"
      pager={{
        page: features.page,
        pages: features.pages ?? 0,
        onChange: features.setPage,
      }}
      getKey={(i) => i.date}
    />
  );
};