import { formatDate } from "../utils.ts";
import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {FeatureItem} from "../types.ts";
import {Fragment} from "react";
import {ReadyStatus} from "../components/ReadyStatus/ReadyStatus.tsx";

const columns: Column<FeatureItem>[] = [
  { key: "date", header: "Дата", render: (i) => formatDate(i.date, "date") },
  { key: "version", header: "Версия", render: (i) => i.version },
  { key: "accidents_lag_1", header: "Лаг 1", render: (i) => i.accidents_lag_1 },
  { key: "accidents_lag_7", header: "Лаг 7", render: (i) => i.accidents_lag_7 },
  { key: "accidents_roll_7", header: "Среднее 7", render: (i) => i.accidents_roll_7 },
  { key: "dow", header: "День недели", render: (i) => i.dow },
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

export const Features = () => {
  const features = useList<FeatureItem>({ url: "/api/features", pageSize: 500 });

  return (
    <Fragment>
      <ReadyStatus
        url="/api/features/ready"
        loaderLabel="Загрузка готовности данных"
      />

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
    </Fragment>

  );
};