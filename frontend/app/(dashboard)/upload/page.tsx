"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { uploadDocument } from "@/api/upload.api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { useUploadSocket } from "@/hooks/use-upload-socket";
import { toast } from "sonner";

type UploadState =
  | "idle"
  | "uploading"
  | "processing"
  | "success"
  | "error";

export default function UploadPage() {
  const router = useRouter();

  const [file, setFile] =
    useState<File | null>(null);

  const [state, setState] =
    useState<UploadState>("idle");

  const [progress, setProgress] =
    useState(0);

  const [hasHeader, setHasHeader] =
    useState(true);

  const [saveMode, setSaveMode] =
    useState<
      "database" | "excel" | "none"
    >("database");

  const { connect } =
    useUploadSocket({
      onProgress: (data) => {
        setState("processing");

        if (
          typeof data.progress ===
          "number"
        ) {
          setProgress(data.progress);
        }
      },

      onComplete: (data) => {
        setState("success");

        toast.success(
          "Upload completed successfully"
        );

        if (data.document_id) {
          setTimeout(() => {
            router.push(
              `/documents/${data.document_id}`
            );
          }, 1000);
        }
      },

      onError: (data) => {
        setState("error");

        toast.error(
          data?.message ||
            "Upload failed"
        );
      },
    });

  const handleUpload =
    useCallback(async () => {
      if (!file) {
        toast.error(
          "Please select a PDF file"
        );
        return;
      }

      try {
        setState("uploading");
        setProgress(0);

        const clientId =
          crypto.randomUUID();

        connect(clientId);

        const response =
          await uploadDocument(
            file,
            clientId,
            hasHeader,
            saveMode
          );

        console.log(
          "UPLOAD RESPONSE",
          response
        );

        if (
          response?.status !==
          "success"
        ) {
          throw new Error(
            response?.message ||
              "Upload failed"
          );
        }
      } catch (error: any) {
        console.error(
          "UPLOAD ERROR",
          error?.response?.data
        );

        setState("error");

        toast.error(
          error?.response?.data
            ?.message ||
            error?.message ||
            "Upload failed"
        );
      }
    }, [
      file,
      hasHeader,
      saveMode,
      connect,
    ]);

  return (
    <div className="max-w-xl space-y-6">
      <h1 className="text-3xl font-bold">
        Upload PDF
      </h1>

      <Input
        type="file"
        accept="application/pdf"
        onChange={(e) =>
          setFile(
            e.target.files?.[0] ||
              null
          )
        }
      />

      <div className="space-y-2">
        <label className="text-sm font-medium">
          Does PDF contain a header
          row?
        </label>

        <select
          value={
            hasHeader
              ? "true"
              : "false"
          }
          onChange={(e) =>
            setHasHeader(
              e.target.value ===
                "true"
            )
          }
          className="w-full border rounded-md p-2"
        >
          <option value="true">
            Yes
          </option>

          <option value="false">
            No
          </option>
        </select>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">
          Save Mode
        </label>

        <select
          value={saveMode}
          onChange={(e) =>
            setSaveMode(
              e.target.value as
                | "database"
                | "excel"
                | "none"
            )
          }
          className="w-full border rounded-md p-2"
        >
          <option value="database">
            Database
          </option>

          <option value="excel">
            Excel
          </option>

          <option value="none">
            Process Only
          </option>
        </select>
      </div>

      <Button
        onClick={handleUpload}
        disabled={
          !file ||
          state === "uploading"
        }
      >
        {state === "uploading"
          ? "Uploading..."
          : "Upload"}
      </Button>

      {(state === "uploading" ||
        state === "processing") && (
        <div className="space-y-2">
          <Progress
            value={progress}
          />

          <p className="text-sm text-muted-foreground">
            {state === "uploading"
              ? "Uploading file..."
              : `Processing PDF... ${progress}%`}
          </p>
        </div>
      )}

      {state === "success" && (
        <p className="text-green-600">
          Upload successful.
        </p>
      )}

      {state === "error" && (
        <p className="text-red-600">
          Upload failed.
        </p>
      )}
    </div>
  );
}