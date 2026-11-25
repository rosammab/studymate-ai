
import api from "./api";

export interface UserProgress {
  total_study_minutes: number;
  total_quizzes: number;
  total_flashcards_reviewed: number;
  current_streak: number;
  longest_streak: number;
  updated_at: string;
}

export interface StudyActivity {
  id: number;
  activity_type: string;
  activity_date: string;
  duration_minutes: number;
  count: number;
  created_at: string;
}

export interface DailyProgress {
  days: number;
  start_date: string;
  end_date: string;
  activities: {
    activity_date: string;
    total_minutes: number;
    activity_count: number;
    total_count: number;
  }[];
}

export interface ActivityBreakdown {
  activity_type: string;
  total_minutes: number;
  total_count: number;
  records: number;
}

export const getProgressSummary = async (): Promise<UserProgress> => {
  const response = await api.get("/progress/summary/");
  return response.data;
};

export const getRecentActivities = async (): Promise<StudyActivity[]> => {
  const response = await api.get("/progress/activities/");
  
  // Supports both a normal list and DRF paginated responses.
  return Array.isArray(response.data)
    ? response.data
    : response.data.results ?? [];
};

export const getDailyProgress = async (
  days = 7
): Promise<DailyProgress> => {
  const response = await api.get(`/progress/daily/?days=${days}`);
  return response.data;
};

export const getActivityBreakdown = async (): Promise<
  ActivityBreakdown[]
> => {
  const response = await api.get("/progress/breakdown/");

  return Array.isArray(response.data)
    ? response.data
    : response.data.results ?? [];
};
