import { type ChangeEvent, useRef, useState } from "react";
import { Button } from "../Button/Button.tsx";
import "./styles.css";

type FileSelectorProps = {
  onUpload: (file: File) => Promise<void>;
  accept?: string;
  buttonText?: string;
  chooseText?: string;
  emptyText?: string;
};

export const FileSelector = ({
  onUpload,
  accept = ".csv",
  buttonText = "Загрузить",
  chooseText = "Выбрать файл",
  emptyText = "Файл не выбран",
}: FileSelectorProps) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] ?? null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    try {
      await onUpload(file);
      setFile(null);
      if (inputRef.current) inputRef.current.value = "";
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="uploader">
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        className="uploader-input"
        disabled={uploading}
      />

      <Button
        onClick={() => inputRef.current?.click()}
        disabled={uploading}
      >
        {chooseText}
      </Button>

      <span className="uploader-name">{file ? file.name : emptyText}</span>

      <Button onClick={handleUpload} disabled={!file} loading={uploading}>
        {buttonText}
      </Button>
    </div>
  );
};