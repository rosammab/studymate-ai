
import { useState, type ChangeEvent, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  FileText,
  FileUp,
  Trash2,
  Eye,
  Search,
  X,
  File,
  CheckCircle,
  AlertCircle,
  Clock,
} from "lucide-react";

import {
  getDocuments,
  uploadDocument,
  deleteDocument,
  type StudyDocument,
} from "../../services/documentService";

import "./Documents.css";

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function StatusBadge({ status }: { status: StudyDocument["status"] }) {
  const statusConfig = {
    pending: { label: "Pending", icon: Clock },
    processing: { label: "Processing", icon: Clock },
    completed: { label: "Completed", icon: CheckCircle },
    failed: { label: "Failed", icon: AlertCircle },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <span className={`document-status ${status}`}>
      <Icon size={14} />
      {config.label}
    </span>
  );
}

export default function Documents() {
  const queryClient = useQueryClient();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [search, setSearch] = useState("");
  const [selectedDocument, setSelectedDocument] =
    useState<StudyDocument | null>(null);
  const [formError, setFormError] = useState("");

  const {
    data: documents = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["documents"],
    queryFn: getDocuments,
  });

  const uploadMutation = useMutation({
    mutationFn: uploadDocument,
    onSuccess: (document) => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      setSelectedFile(null);
      setTitle("");
      setFormError("");

      if (document.status === "failed") {
        setFormError(
          document.error_message || "Document text extraction failed."
        );
      }
    },
    onError: () => {
      setFormError("Unable to upload document. Please try again.");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });

      if (selectedDocument) {
        setSelectedDocument(null);
      }
    },
    onError: () => {
      setFormError("Unable to delete document.");
    },
  });

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;

    setFormError("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    const extension = file.name.split(".").pop()?.toLowerCase();

    if (!["pdf", "docx"].includes(extension || "")) {
      setFormError("Only PDF and DOCX files are supported.");
      setSelectedFile(null);
      event.target.value = "";
      return;
    }

    if (file.size === 0) {
      setFormError("Empty files cannot be uploaded.");
      setSelectedFile(null);
      event.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setFormError("File size cannot exceed 10 MB.");
      setSelectedFile(null);
      event.target.value = "";
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedFile) {
      setFormError("Please select a PDF or DOCX file.");
      return;
    }

    setFormError("");

    uploadMutation.mutate({
      title: title.trim(),
      file: selectedFile,
    });
  };

  const filteredDocuments = documents.filter((document) =>
    document.title.toLowerCase().includes(search.toLowerCase())
  );

  const handleDelete = (document: StudyDocument) => {
    if (window.confirm(`Delete "${document.title}"?`)) {
      deleteMutation.mutate(document.id);
    }
  };

  if (isLoading) {
    return <div className="document-message">Loading documents...</div>;
  }

  if (isError) {
    return (
      <div className="document-message document-error">
        Unable to load documents. Please check your connection.
      </div>
    );
  }

  return (
    <div className="documents-page">
      <div className="documents-header">
        <div>
          <h1>My Documents</h1>
          <p>Upload and manage your study materials.</p>
        </div>

        <div className="document-total">
          <FileText size={19} />
          {documents.length} Documents
        </div>
      </div>

      {/* Upload form */}
      <form className="document-upload-card" onSubmit={handleUpload}>
        <div className="upload-heading">
          <div className="upload-icon">
            <FileUp size={25} />
          </div>

          <div>
            <h2>Upload Study Document</h2>
            <p>Supported formats: PDF and DOCX. Maximum size: 10 MB.</p>
          </div>
        </div>

        <label className="document-field-label">
          Document title (optional)
        </label>

        <input
          className="document-title-input"
          type="text"
          placeholder="Enter document title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          maxLength={255}
        />

        <label className="document-field-label">
          Select your document
        </label>

        <div className="document-file-input">
          <input
            id="study-document-file"
            type="file"
            accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            onChange={handleFileChange}
          />

          <label htmlFor="study-document-file">
            <FileUp size={20} />
            Choose PDF or DOCX
          </label>

          {selectedFile && (
            <div className="selected-file">
              <File size={17} />
              <span>{selectedFile.name}</span>
              <small>{formatFileSize(selectedFile.size)}</small>
            </div>
          )}
        </div>

        {formError && (
          <div className="document-form-error">
            <AlertCircle size={17} />
            {formError}
          </div>
        )}

        <button
          className="document-upload-button"
          type="submit"
          disabled={!selectedFile || uploadMutation.isPending}
        >
          <FileUp size={18} />
          {uploadMutation.isPending
            ? "Uploading and extracting text..."
            : "Upload Document"}
        </button>
      </form>

      {/* Document list */}
      <div className="document-list-header">
        <div>
          <h2>Uploaded Documents</h2>
          <p>View your uploaded study materials and extracted text.</p>
        </div>

        <div className="document-search">
          <Search size={17} />
          <input
            type="text"
            placeholder="Search documents..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>
      </div>

      <div className="document-list">
        {filteredDocuments.length === 0 ? (
          <div className="document-empty">
            <FileText size={42} />
            <h3>No documents found</h3>
            <p>
              {search
                ? "Try another search term."
                : "Upload your first study document to get started."}
            </p>
          </div>
        ) : (
          filteredDocuments.map((document) => (
            <div className="document-row" key={document.id}>
              <div className="document-file-icon">
                <FileText size={24} />
              </div>

              <div className="document-info">
                <h3>{document.title}</h3>

                <p>
                  {document.file_type.toUpperCase()} ·{" "}
                  {formatFileSize(document.file_size)} ·{" "}
                  {new Date(document.created_at).toLocaleDateString()}
                </p>

                <StatusBadge status={document.status} />

                {document.status === "failed" && (
                  <p className="document-row-error">
                    {document.error_message}
                  </p>
                )}
              </div>

              <div className="document-actions">
                <button
                  title="View extracted text"
                  onClick={() => setSelectedDocument(document)}
                  disabled={document.status !== "completed"}
                >
                  <Eye size={18} />
                  <span>View Text</span>
                </button>

                <button
                  className="document-delete-button"
                  title="Delete document"
                  onClick={() => handleDelete(document)}
                  disabled={deleteMutation.isPending}
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Extracted text modal */}
      {selectedDocument && (
        <div
          className="document-modal-overlay"
          onClick={() => setSelectedDocument(null)}
        >
          <div
            className="document-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="document-modal-header">
              <div>
                <h2>{selectedDocument.title}</h2>
                <p>Extracted document text</p>
              </div>

              <button
                onClick={() => setSelectedDocument(null)}
                title="Close"
              >
                <X size={21} />
              </button>
            </div>

            <div className="document-extracted-text">
              {selectedDocument.extracted_text || "No extracted text available."}
            </div>

            <div className="document-modal-footer">
              <button
                onClick={() => setSelectedDocument(null)}
                className="document-upload-button"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
