
import api from "./api";

// ==========================================
// TYPES / INTERFACES
// ==========================================

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface SendMessageResponse {
  conversation_id: number;
  user_message: ChatMessage;
  assistant_message: ChatMessage;
}

export interface GeneratedArtifactResponse {
  message: string;
  id: number;
  title: string;
  file_url: string;
  created_at: string;
}

interface PaginatedResponse<T> {
  results: T[];
}

// ==========================================
// HELPER FUNCTION
// ==========================================

function extractList<T>(
  data: T[] | PaginatedResponse<T>
): T[] {
  if (Array.isArray(data)) {
    return data;
  }

  return data.results ?? [];
}

// ==========================================
// CONVERSATIONS
// ==========================================

// Get all conversations
export const getConversations = async (): Promise<Conversation[]> => {
  const response = await api.get<
    Conversation[] | PaginatedResponse<Conversation>
  >("/ai-assistant/conversations/");

  return extractList(response.data);
};

// Create a new conversation
export const createConversation = async (
  title = "New conversation"
): Promise<Conversation> => {
  const response = await api.post<Conversation>(
    "/ai-assistant/conversations/",
    { title }
  );

  return response.data;
};

// Delete a conversation
export const deleteConversation = async (
  conversationId: number
): Promise<void> => {
  await api.delete(
    `/ai-assistant/conversations/${conversationId}/`
  );
};

// ==========================================
// CHAT MESSAGES
// ==========================================

// Get messages of a conversation
export const getMessages = async (
  conversationId: number
): Promise<ChatMessage[]> => {
  const response = await api.get<
    ChatMessage[] | PaginatedResponse<ChatMessage>
  >(
    `/ai-assistant/conversations/${conversationId}/messages/`
  );

  return extractList(response.data);
};

// Send a message to Gemini through Django
export const sendMessage = async (
  conversationId: number,
  content: string
): Promise<SendMessageResponse> => {
  const response = await api.post<SendMessageResponse>(
    `/ai-assistant/conversations/${conversationId}/messages/`,
    {
      content: content.trim(),
    }
  );

  return response.data;
};

// ==========================================
// PDF GENERATION
// ==========================================

export const generatePDF = async (
  prompt: string
): Promise<GeneratedArtifactResponse> => {
  const response = await api.post<GeneratedArtifactResponse>(
    "/ai-assistant/generate-pdf/",
    {
      prompt: prompt.trim(),
    }
  );

  return response.data;
};

// ==========================================
// IMAGE GENERATION
// ==========================================

export const generateImage = async (
  prompt: string
): Promise<GeneratedArtifactResponse> => {
  const response = await api.post<GeneratedArtifactResponse>(
    "/ai-assistant/generate-image/",
    {
      prompt: prompt.trim(),
    }
  );

  return response.data;
};