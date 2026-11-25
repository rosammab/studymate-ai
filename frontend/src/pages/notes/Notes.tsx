
import { useState, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Plus,
  Search,
  FileText,
  Pencil,
  Trash2,
  X,
  Save,
} from "lucide-react";

import {
  getNotes,
  createNote,
  updateNote,
  deleteNote,
  type Note,
  type NoteFormData,
} from "../../services/noteService";

import "./Notes.css";

const emptyForm: NoteFormData = {
  title: "",
  content: "",
};

export default function Notes() {
  const queryClient = useQueryClient();

  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingNote, setEditingNote] = useState<Note | null>(null);
  const [form, setForm] = useState<NoteFormData>(emptyForm);
  const [formError, setFormError] = useState("");

  // Retrieve notes from Django
  const {
    data: notes = [],
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["notes"],
    queryFn: getNotes,
  });

  // Create note mutation
  const createMutation = useMutation({
    mutationFn: createNote,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notes"] });
      closeForm();
    },
    onError: () => {
      setFormError("Unable to create note. Please try again.");
    },
  });

  // Update note mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: NoteFormData }) =>
      updateNote(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notes"] });
      closeForm();
    },
    onError: () => {
      setFormError("Unable to update note. Please try again.");
    },
  });

  // Delete note mutation
  const deleteMutation = useMutation({
    mutationFn: deleteNote,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notes"] });
    },
  });

  const closeForm = () => {
    setShowForm(false);
    setEditingNote(null);
    setForm(emptyForm);
    setFormError("");
  };

  const openCreateForm = () => {
    setEditingNote(null);
    setForm(emptyForm);
    setFormError("");
    setShowForm(true);
  };

  const openEditForm = (note: Note) => {
    setEditingNote(note);
    setForm({
      title: note.title,
      content: note.content,
    });
    setFormError("");
    setShowForm(true);
  };

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError("");

    if (!form.title.trim() || !form.content.trim()) {
      setFormError("Both title and content are required.");
      return;
    }

    const data = {
      title: form.title.trim(),
      content: form.content.trim(),
    };

    if (editingNote) {
      updateMutation.mutate({
        id: editingNote.id,
        data,
      });
    } else {
      createMutation.mutate(data);
    }
  };

  const handleDelete = (note: Note) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${note.title}"?`
    );

    if (confirmed) {
      deleteMutation.mutate(note.id);
    }
  };

  const filteredNotes = notes.filter((note) => {
    const query = search.toLowerCase();

    return (
      note.title.toLowerCase().includes(query) ||
      note.content.toLowerCase().includes(query)
    );
  });

  const isSaving = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="notes-page">
      <div className="notes-header">
        <div>
          <p className="eyebrow">MY LEARNING SPACE</p>
          <h1>My Notes</h1>
          <p className="notes-subtitle">
            Create and organize your study notes in one place.
          </p>
        </div>

        <button className="notes-primary-button" onClick={openCreateForm}>
          <Plus size={18} />
          Create Note
        </button>
      </div>

      <div className="notes-toolbar">
        <div className="notes-search">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search your notes..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>

        <span className="notes-count">
          {notes.length} {notes.length === 1 ? "note" : "notes"}
        </span>
      </div>

      {showForm && (
        <section className="note-form-card">
          <div className="note-form-heading">
            <h2>{editingNote ? "Edit Note" : "Create New Note"}</h2>

            <button
              className="note-close-button"
              onClick={closeForm}
              type="button"
              aria-label="Close form"
            >
              <X size={20} />
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            <label htmlFor="note-title">Note Title</label>
            <input
              id="note-title"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="Enter your note title"
              maxLength={200}
              required
            />

            <label htmlFor="note-content">Note Content</label>
            <textarea
              id="note-content"
              name="content"
              value={form.content}
              onChange={handleChange}
              placeholder="Write your study notes here..."
              rows={7}
              required
            />

            {formError && (
              <p className="notes-error">{formError}</p>
            )}

            <div className="note-form-actions">
              <button
                type="button"
                className="notes-cancel-button"
                onClick={closeForm}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="notes-primary-button"
                disabled={isSaving}
              >
                <Save size={17} />
                {isSaving
                  ? "Saving..."
                  : editingNote
                    ? "Update Note"
                    : "Save Note"}
              </button>
            </div>
          </form>
        </section>
      )}

      {isLoading ? (
        <div className="notes-message">Loading your notes...</div>
      ) : isError ? (
        <div className="notes-message notes-error">
          {(error as Error).message || "Unable to load notes. Please log in again."}
        </div>
      ) : filteredNotes.length === 0 ? (
        <div className="notes-empty">
          <FileText size={42} />
          <h2>{search ? "No matching notes" : "No notes yet"}</h2>
          <p>
            {search
              ? "Try a different search term."
              : "Create your first study note to get started."}
          </p>

          {!search && (
            <button className="notes-primary-button" onClick={openCreateForm}>
              <Plus size={18} />
              Create Your First Note
            </button>
          )}
        </div>
      ) : (
        <div className="notes-grid">
          {filteredNotes.map((note) => (
            <article className="note-card" key={note.id}>
              <div className="note-card-top">
                <div className="note-card-icon">
                  <FileText size={21} />
                </div>

                <div className="note-actions">
                  <button
                    onClick={() => openEditForm(note)}
                    aria-label={`Edit ${note.title}`}
                    title="Edit note"
                  >
                    <Pencil size={17} />
                  </button>

                  <button
                    onClick={() => handleDelete(note)}
                    aria-label={`Delete ${note.title}`}
                    title="Delete note"
                    disabled={deleteMutation.isPending}
                  >
                    <Trash2 size={17} />
                  </button>
                </div>
              </div>

              <h2>{note.title}</h2>

              <p className="note-card-content">
                {note.content}
              </p>

              <div className="note-card-footer">
                <span>
                  Updated: {new Date(note.updated_at).toLocaleDateString()}
                </span>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
