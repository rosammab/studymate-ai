
import api from "./api";

export interface Quiz {
  id: number;
  user: string;
  title: string;
  description: string;
  question_count: number;
  created_at: string;
  updated_at: string;
}

export interface QuizOption {
  id: number;
  option_text: string;
}

export interface QuizQuestion {
  id: number;
  question_text: string;
  marks: number;
  options: QuizOption[];
}

export interface QuizDetails {
  id: number;
  user: string;
  title: string;
  description: string;
  questions: QuizQuestion[];
  created_at: string;
}

export interface QuizFormData {
  title: string;
  description: string;
}

export interface QuestionFormData {
  question_text: string;
  marks: number;
}

export interface OptionFormData {
  option_text: string;
  is_correct: boolean;
}

export interface QuizSubmissionData {
  answers: {
    question: number;
    selected_option: number | null;
  }[];
}

export interface QuizSubmissionResult {
  message: string;
  attempt_id: number;
  score: number;
  total_marks: number;
  percentage: number;
  correct_answers: number;
  total_questions: number;
  progress_updated: boolean;
  notification_created: boolean;
}

export interface QuizAttemptAnswer {
  id: number;
  question: number;
  question_text: string;
  selected_option: number | null;
  selected_option_text: string | null;
  is_correct: boolean;
}

export interface QuizAttempt {
  id: number;
  quiz: number;
  quiz_title: string;
  score: number;
  total_marks: number;
  submitted_at: string;
  answers: QuizAttemptAnswer[];
}

function extractList<T>(data: T[] | { results: T[] }): T[] {
  return Array.isArray(data) ? data : data.results;
}

// Quiz CRUD
export const getQuizzes = async (): Promise<Quiz[]> => {
  const response = await api.get("/quizzes/");
  return extractList<Quiz>(response.data);
};

export const createQuiz = async (
  data: QuizFormData
): Promise<Quiz> => {
  const response = await api.post("/quizzes/", data);
  return response.data;
};

export const updateQuiz = async ({
  id,
  data,
}: {
  id: number;
  data: QuizFormData;
}): Promise<Quiz> => {
  const response = await api.patch(`/quizzes/${id}/`, data);
  return response.data;
};

export const deleteQuiz = async (id: number): Promise<void> => {
  await api.delete(`/quizzes/${id}/`);
};

export const getQuizDetails = async (
  id: number
): Promise<QuizDetails> => {
  const response = await api.get(`/quizzes/${id}/`);
  return response.data;
};

// Questions
export const getQuestions = async (
  quizId: number
): Promise<QuizQuestion[]> => {
  const response = await api.get(`/quizzes/${quizId}/questions/`);
  return extractList<QuizQuestion>(response.data);
};

export const createQuestion = async ({
  quizId,
  data,
}: {
  quizId: number;
  data: QuestionFormData;
}) => {
  const response = await api.post(
    `/quizzes/${quizId}/questions/create/`,
    data
  );
  return response.data;
};

// Options
export const createQuizOption = async ({
  questionId,
  data,
}: {
  questionId: number;
  data: OptionFormData;
}) => {
  const response = await api.post(
    `/quizzes/questions/${questionId}/options/create/`,
    data
  );
  return response.data;
};

// Submission
export const submitQuiz = async ({
  quizId,
  data,
}: {
  quizId: number;
  data: QuizSubmissionData;
}): Promise<QuizSubmissionResult> => {
  const response = await api.post(
    `/quizzes/${quizId}/submit/`,
    data
  );
  return response.data;
};

// Attempts
export const getQuizAttempts = async (
  quizId?: number
): Promise<QuizAttempt[]> => {
  const response = await api.get(
    "/quizzes/attempts/",
    quizId ? { params: { quiz: quizId } } : undefined
  );
  return extractList<QuizAttempt>(response.data);
};

export const getQuizAttempt = async (
  id: number
): Promise<QuizAttempt> => {
  const response = await api.get(`/quizzes/attempts/${id}/`);
  return response.data;
};
