import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type {ModelItem} from "../types.ts";
import {formatDate} from "../utils.ts";
import {Button} from "../components/Button/Button.tsx";
import {useState} from "react";

const columns: Column<ModelItem>[] = [
  { key: "id", header: "№", render: (i) => i.id},
  { key: "feature_version", header: "Версия данных", render: (i) => i.feature_version},
  { key: "random_seed", header: "Рандом", render: (i) => i.random_seed},
  { key: "params", header: "Гиперпараметры", render: (i) => "123"},
  { key: "train_start", header: "Начало обучения", render: (i) => formatDate(i.train_start)},
  { key: "train_end", header: "Конец обучения", render: (i) => formatDate(i.train_end)},
  { key: "test_start", header: "Начало оценки", render: (i) => formatDate(i.test_start)},
  { key: "test_end", header: "Конец оценки", render: (i) => formatDate(i.test_end)},
  { key: "n_train", header: "Количество обучающих записей", render: (i) => i.n_train},
  { key: "n_test", header: "Количество тестовых записей", render: (i) => i.n_test},
  { key: "mae_train", header: "MAE обучения", render: (i) => i.mae_train},
  { key: "mae_test", header: "MAE тест", render: (i) => i.mae_test},
  { key: "mase_train", header: "MASE обучения", render: (i) => i.mase_train},
  { key: "mase_test", header: "MASE тест", render: (i) => i.mase_test},
];

export const BaseModel = () => {
  const weather = useList<ModelItem>({ url: "/api/runs", modelId: 1 });

  const [isRunning, setIsRunning] = useState<boolean>(false)
  const handleStart = async () => {
    setIsRunning(true)
    try {
      const params = new URLSearchParams({ model_id: `1` });
      await fetch(`/api/model_start?${params}`);
    } finally {
      setIsRunning(false)
    }
  };

  return (
    <div>
      <Button
        onClick={handleStart}
        disabled={isRunning}
        loading={isRunning}
      >
        Запустить модель
      </Button>
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
        getKey={(i) => i.id}
      />
    </div>
  );
};