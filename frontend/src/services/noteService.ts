import api from "./api";

export interface Note {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface NoteFormData {
  title: string;
  content: string;
}

// Get all notes belonging to the logged-in user
export const getNotes = async (): Promise<Note[]> => {
  const response = await api.get("/notes/");

  return Array.isArray(response.data)
    ? response.data
    : response.data.results ?? [];
};

// Create a new note
export const createNote = async (
  data: NoteFormData
): Promise<Note> => {
  const response = await api.post("/notes/", data);
  return response.data;
};

// Update an existing note
export const updateNote = async (
  id: number,
  data: NoteFormData
): Promise<Note> => {
  const response = await api.patch(`/notes/${id}/`, data);
  return response.data;
};

// Delete a note
export const deleteNote = async (id: number): Promise<void> => {
  await api.delete(`/notes/${id}/`);
};