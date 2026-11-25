
import api from "./api";

export interface StudyDocument {
  id: number;
  title: string;
  file: string;
  file_type: "pdf" | "docx";
  file_size: number;
  extracted_text: string;
  status: "pending" | "processing" | "completed" | "failed";
  error_message: string;
  created_at: string;
  updated_at: string;
}

export interface DocumentUploadData {
  title?: string;
  file: File;
}

function extractList<T>(data: T[] | { results: T[] }): T[] {
  return Array.isArray(data) ? data : data.results;
}

// Get all documents
export const getDocuments = async (): Promise<StudyDocument[]> => {
  const response = await api.get("/documents/");
  return extractList<StudyDocument>(response.data);
};

// Upload document
export const uploadDocument = async (
  data: DocumentUploadData
): Promise<StudyDocument> => {
  const formData = new FormData();

  if (data.title?.trim()) {
    formData.append("title", data.title.trim());
  }

  formData.append("file", data.file);

  const response = await api.post("/documents/", formData);

  return response.data;
};

// Get document details
export const getDocumentDetails = async (
  id: number
): Promise<StudyDocument> => {
  const response = await api.get(`/documents/${id}/`);
  return response.data;
};

// Delete document
export const deleteDocument = async (id: number): Promise<void> => {
  await api.delete(`/documents/${id}/`);
};
