import {type ChangeEvent, useState} from "react";
export const Uploader = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadLoading, setUploadLoading] = useState<boolean>(false);

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
      setUploadLoading(false);
    }
  };

  return (
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
  );
};
