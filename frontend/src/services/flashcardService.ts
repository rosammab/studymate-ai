
import api from "./api";

export interface Flashcard {
  id: number;
  question: string;
  answer: string;
  created_at: string;
  updated_at: string;
}

export interface FlashcardSet {
  id: number;
  title: string;
  description: string;
  cards: Flashcard[];
  created_at: string;
  updated_at: string;
}

export interface FlashcardSetForm {
  title: string;
  description: string;
}

export interface FlashcardForm {
  question: string;
  answer: string;
}

export interface FlashcardReview {
  id: number;
  flashcard: number;
  result: "known" | "missed";
  reviewed_at: string;
}

function extractList<T>(data: T[] | { results: T[] }): T[] {
  return Array.isArray(data) ? data : data.results;
}

// Flashcard sets
export const getFlashcardSets = async (): Promise<FlashcardSet[]> => {
  const response = await api.get("/flashcards/sets/");
  return extractList<FlashcardSet>(response.data);
};

export const createFlashcardSet = async (
  data: FlashcardSetForm
): Promise<FlashcardSet> => {
  const response = await api.post("/flashcards/sets/", data);
  return response.data;
};

export const updateFlashcardSet = async ({
  id,
  data,
}: {
  id: number;
  data: FlashcardSetForm;
}): Promise<FlashcardSet> => {
  const response = await api.patch(`/flashcards/sets/${id}/`, data);
  return response.data;
};

export const deleteFlashcardSet = async (id: number): Promise<void> => {
  await api.delete(`/flashcards/sets/${id}/`);
};

// Cards
export const getFlashcards = async (
  setId: number
): Promise<Flashcard[]> => {
  const response = await api.get(`/flashcards/sets/${setId}/cards/`);
  return extractList<Flashcard>(response.data);
};

export const createFlashcard = async ({
  setId,
  data,
}: {
  setId: number;
  data: FlashcardForm;
}): Promise<Flashcard> => {
  const response = await api.post(
    `/flashcards/sets/${setId}/cards/`,
    data
  );
  return response.data;
};

export const updateFlashcard = async ({
  id,
  data,
}: {
  id: number;
  data: FlashcardForm;
}): Promise<Flashcard> => {
  const response = await api.patch(`/flashcards/cards/${id}/`, data);
  return response.data;
};

export const deleteFlashcard = async (id: number): Promise<void> => {
  await api.delete(`/flashcards/cards/${id}/`);
};

// Reviews
export const createFlashcardReview = async (
  flashcard: number,
  result: "known" | "missed"
): Promise<FlashcardReview> => {
  const response = await api.post("/flashcards/reviews/create/", {
    flashcard,
    result,
  });
  return response.data;
};

export const getFlashcardReviews = async (): Promise<FlashcardReview[]> => {
  const response = await api.get("/flashcards/reviews/");
  return extractList<FlashcardReview>(response.data);
};
