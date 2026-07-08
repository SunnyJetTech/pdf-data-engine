import apiClient from "@/lib/axios";

export async function uploadDocument(file: File, clientId: string, hasHeader: boolean, saveMode: "database" | "excel" | "none") {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("client_id", clientId);
  formData.append("has_header", String(hasHeader));
  formData.append("save_mode", saveMode);

  const response = await apiClient.post("/pdf/upload", formData, {
      headers: {
        "Content-Type":
          "multipart/form-data",
      },
    }
  );

  return response.data;
}