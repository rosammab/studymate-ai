import api from "./api";

export interface LoginData {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  phone_number: string;
  university: string;
  course: string;
  year_of_study: string;
  state: string;
  country: string;
  board: string;
  preferred_language: string;
  bio?: string;
  study_goal?: string;
}

export const loginUser = async (
  data: LoginData
): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>(
    "/auth/login/",
    data
  );

  return response.data;
};

export const registerUser = async (data: RegisterData) => {
  const response = await api.post("/register/", data);
  return response.data;
};

export const getUserProfile = async () => {
  const response = await api.get("/profile/");
  return response.data;
};

export const logoutUser = async (refresh: string) => {
  const response = await api.post("/auth/logout/", {
    refresh,
  });

  return response.data;
};