import {type ChangeEvent, Fragment, useEffect, useState} from "react";
import type {DataPage} from "../types.ts";
import {formatDate} from "../utils.ts";

const STATUS_LABELS: Record<string, string> = {
  ok: "Успешно",
  empty: "Пустой файл",
  error: "Ошибка",
};

export const Uploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadLoading, setUploadLoading] = useState<boolean>(false);

  const [data, setData] = useState<DataPage>({
    items: [],
    total: 0,
  });
  const [dataLoading, setDataLoading] = useState<boolean>(false);


  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] ?? null);
  };

  const upload = async () => {
    if (!file) return;

    setUploadLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => null);
        alert(`Ошибка при загрузке: ${err?.detail ?? res.status}`);
        return;
      }
    } catch {
      alert("Нет связи с сервером");
    } finally {
      loadData()
      setUploadLoading(false);
    }
  };

    const loadData = async (): Promise<void> => {
      setDataLoading(true);

      try {
        const res = await fetch(`/api/load_log`);

        if (!res.ok) {
          alert("Ошибка при загрузке");
          return;
        }

        const result: DataPage = await res.json();
        setData(result);
      } catch {
        alert("Нет связи с сервером");
      } finally {
        setDataLoading(false);
      }
  };

  useEffect(() => {
    loadData()
  }, [])

  const { items, total} = data;

  return (
    <Fragment>
      <div className="uploader">
        <input
          type="file"
          accept=".csv"
          onChange={handleChange}
          className="uploader-file"
          disabled={uploadLoading}
        />

        <button
          onClick={upload}
          disabled={uploadLoading || !file}
          className="uploader-button"
        >
          Загрузить
        </button>

        {uploadLoading && <span className="uploader-status">Загрузка...</span>}
      </div>

      <div className="list-wrapper">
      <div className="list-meta-header">
        <div className="list-total">
          Всего записей: {total.toLocaleString("ru-RU")}
        </div>
      </div>

      {dataLoading && <div className="list-status">Загрузка данных...</div>}

     <div className="list-table-wrap">
          <table className="list-table">
            <thead>
              <tr>
                <th>Начало</th>
                <th>Окончание</th>
                <th>Файл</th>
                <th>Статус</th>
                <th className="num">Строк в файле</th>
                <th className="num">Вставлено</th>
                <th>Ошибка</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>{formatDate(item.started_at)}</td>
                  <td>{formatDate(item.finished_at)}</td>
                  <td className="list-address" title={item.file_name ?? ""}>
                    {item.file_name ?? "—"}
                  </td>
                  <td className={`list-status-${item.status}`}>
                    {STATUS_LABELS[item.status] ?? item.status}
                  </td>
                  <td className="num">{item.rows_total}</td>
                  <td className="num">{item.rows_inserted}</td>
                  <td className="list-address" title={item.error ?? ""}>
                    {item.error ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {items.length === 0 && !dataLoading && (
            <div className="list-empty">Загрузок пока не было</div>
          )}
        </div>
      </div>
    </Fragment>
  );
};
