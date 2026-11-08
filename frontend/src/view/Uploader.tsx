import { formatDate } from "../utils.ts";
import { FileSelector } from "../components/FileSelector/FileSelector.tsx";
import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type { LoadLogItem } from "../types.ts";

const STATUS_LABELS: Record<string, string> = {
  ok: "Успешно",
  empty: "Пустой файл",
  error: "Ошибка",
};

const columns: Column<LoadLogItem>[] = [
  { key: "started", header: "Начало", render: (i) => formatDate(i.started_at) },
  { key: "finished", header: "Окончание", render: (i) => formatDate(i.finished_at) },
  {
    key: "file",
    header: "Файл",
    render: (i) => i.file_name ?? "—",
    className: "list-address",
  },
  {
    key: "status",
    header: "Статус",
    render: (i) => (
      <span className={`list-status-${i.status}`}>
        {STATUS_LABELS[i.status] ?? i.status}
      </span>
    ),
  },
  { key: "total", header: "Строк в файле", align: "right", render: (i) => i.rows_total },
  { key: "inserted", header: "Вставлено", align: "right", render: (i) => i.rows_inserted },
  {
    key: "error",
    header: "Ошибка",
    render: (i) => i.error ?? "—",
    className: "list-address",
  },
];

export const Uploader = () => {
  const log = useList<LoadLogItem>({ url: "/api/load_log" });

  const upload = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/upload", { method: "POST", body: formData });
      if (!res.ok) {
        const err = await res.json().catch(() => null);
        alert(`Ошибка при загрузке: ${err?.detail ?? res.status}`);
      }
    } catch {
      alert("Нет связи с сервером");
    } finally {
      log.reload();
    }
  };

  return (
    <>
      <FileSelector onUpload={upload} />

      <List
        items={log.items}
        total={log.total}
        columns={columns}
        loading={log.loading}
        emptyText="Загрузок пока не было"
      />
    </>
  );
};