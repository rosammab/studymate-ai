
import { useEffect, useRef, useState } from "react";
import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  Bot,
  Send,
  Plus,
  Trash2,
  MessageSquare,
  User,
  Loader2,
  Sparkles,
  GraduationCap,
} from "lucide-react";

import {
  getConversations,
  createConversation,
  getMessages,
  sendMessage,
  deleteConversation,
} from "../../services/aiAssistantService";

import type {
  Conversation,
  ChatMessage,
} from "../../services/aiAssistantService";

import "./AIAssistant.css";

const AIAssistant = () => {
  const queryClient = useQueryClient();

  const [selectedConversation, setSelectedConversation] =
    useState<number | null>(null);

  const [message, setMessage] = useState("");

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Fetch all conversations
  const {
    data: conversations = [],
    isLoading: conversationsLoading,
    isError: conversationsError,
  } = useQuery({
    queryKey: ["ai-conversations"],
    queryFn: getConversations,
  });

  // Fetch messages for the selected conversation
  const {
    data: messages = [],
    isLoading: messagesLoading,
  } = useQuery({
    queryKey: ["ai-messages", selectedConversation],
    queryFn: () => getMessages(selectedConversation!),
    enabled: selectedConversation !== null,
  });

  // Automatically select the first conversation
  useEffect(() => {
    if (
      selectedConversation === null &&
      conversations.length > 0
    ) {
      setSelectedConversation(conversations[0].id);
    }
  }, [conversations, selectedConversation]);

  // Scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  // Create conversation mutation
  const createMutation = useMutation({
    mutationFn: () => createConversation(),

    onSuccess: async (conversation) => {
      await queryClient.invalidateQueries({
        queryKey: ["ai-conversations"],
      });

      setSelectedConversation(conversation.id);
    },
  });

  // Send message mutation
  const sendMutation = useMutation({
    mutationFn: ({
      conversationId,
      content,
    }: {
      conversationId: number;
      content: string;
    }) => sendMessage(conversationId, content),

    onSuccess: async (_, variables) => {
      await Promise.all([
        queryClient.invalidateQueries({
          queryKey: [
            "ai-messages",
            variables.conversationId,
          ],
        }),

        queryClient.invalidateQueries({
          queryKey: ["ai-conversations"],
        }),
      ]);
    },
  });

  // Delete conversation mutation
  const deleteMutation = useMutation({
    mutationFn: deleteConversation,

    onSuccess: async (_, deletedId) => {
      await queryClient.invalidateQueries({
        queryKey: ["ai-conversations"],
      });

      queryClient.removeQueries({
        queryKey: ["ai-messages", deletedId],
      });

      if (selectedConversation === deletedId) {
        setSelectedConversation(null);
      }
    },
  });

  // Create a new chat
  const handleNewConversation = () => {
    if (createMutation.isPending) return;

    createMutation.mutate();
  };

  // Send message
  const handleSendMessage = () => {
    const content = message.trim();

    if (
      !content ||
      selectedConversation === null ||
      sendMutation.isPending
    ) {
      return;
    }

    sendMutation.mutate({
      conversationId: selectedConversation,
      content,
    });

    setMessage("");
  };

  // Handle Enter key
  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleDeleteConversation = (
    event: React.MouseEvent<HTMLButtonElement>,
    conversationId: number
  ) => {
    event.stopPropagation();

    const confirmed = window.confirm(
      "Are you sure you want to delete this conversation?"
    );

    if (confirmed) {
      deleteMutation.mutate(conversationId);
    }
  };

  const selectedChat = conversations.find(
    (conversation) =>
      conversation.id === selectedConversation
  );

  const isBusy =
    sendMutation.isPending ||
    createMutation.isPending;

  return (
    <div className="ai-page">

      {/* Sidebar */}
      <aside className="ai-sidebar">

        <div className="ai-sidebar-header">
          <div className="ai-brand">
            <div className="ai-brand-icon">
              <GraduationCap size={24} />
            </div>

            <div>
              <h2>StudyMate AI</h2>
              <span>Your study companion</span>
            </div>
          </div>

          <button
            className="ai-new-chat"
            onClick={handleNewConversation}
            disabled={createMutation.isPending}
          >
            {createMutation.isPending ? (
              <Loader2 size={17} className="ai-spin" />
            ) : (
              <Plus size={17} />
            )}

            New Chat
          </button>
        </div>

        <div className="ai-history">

          <h4>RECENT CONVERSATIONS</h4>

          {conversationsLoading && (
            <p className="ai-muted">Loading conversations...</p>
          )}

          {conversationsError && (
            <p className="ai-error">
              Could not load conversations.
            </p>
          )}

          {!conversationsLoading &&
            conversations.length === 0 && (
              <p className="ai-muted">
                No conversations yet. Start a new chat!
              </p>
            )}

          {conversations.map((conversation: Conversation) => (
            <div
              key={conversation.id}
              className={`ai-history-item ${
                selectedConversation === conversation.id
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                setSelectedConversation(conversation.id)
              }
            >
              <MessageSquare size={17} />

              <span title={conversation.title}>
                {conversation.title}
              </span>

              <button
                className="ai-delete-button"
                onClick={(event) =>
                  handleDeleteConversation(
                    event,
                    conversation.id
                  )
                }
                disabled={deleteMutation.isPending}
                title="Delete conversation"
              >
                <Trash2 size={15} />
              </button>
            </div>
          ))}
        </div>

        <div className="ai-sidebar-footer">
          <Sparkles size={16} />
          <span>Powered by Gemini</span>
        </div>

      </aside>

      {/* Main chat area */}
      <main className="ai-main">

        <header className="ai-topbar">
          <div>
            <h3>
              {selectedChat?.title || "AI Assistant"}
            </h3>

            <span>
              <span className="ai-status-dot"></span>
              Your personal learning assistant
            </span>
          </div>
        </header>

        <div className="ai-chat-area">

          {/* Empty state */}
          {selectedConversation === null && (
            <div className="ai-welcome">
              <div className="ai-welcome-icon">
                <Bot size={38} />
              </div>

              <h1>How can I help you study today?</h1>

              <p>
                Ask questions, understand difficult topics,
                prepare for exams, or explore new concepts.
              </p>

              <button
                onClick={handleNewConversation}
                disabled={createMutation.isPending}
              >
                <Plus size={18} />
                Start a conversation
              </button>
            </div>
          )}

          {/* Messages */}
          {selectedConversation !== null && (
            <div className="ai-messages">

              {messagesLoading && (
                <div className="ai-loading">
                  <Loader2 className="ai-spin" size={22} />
                  Loading messages...
                </div>
              )}

              {!messagesLoading &&
                messages.length === 0 && (
                  <div className="ai-welcome ai-welcome-small">
                    <div className="ai-welcome-icon">
                      <Bot size={34} />
                    </div>

                    <h1>Start learning with StudyMate AI</h1>

                    <p>
                      Ask me anything about your studies.
                      I'm here to help!
                    </p>
                  </div>
                )}

              {messages.map((chat: ChatMessage) => (
                <div
                  key={chat.id}
                  className={`ai-message-row ${
                    chat.role === "user"
                      ? "user-message"
                      : "assistant-message"
                  }`}
                >
                  <div className="ai-avatar">
                    {chat.role === "user" ? (
                      <User size={19} />
                    ) : (
                      <Bot size={20} />
                    )}
                  </div>

                  <div className="ai-message-content">
                    <span className="ai-message-author">
                      {chat.role === "user"
                        ? "You"
                        : "StudyMate AI"}
                    </span>

                    <div className="ai-message-bubble">
                      {chat.content}
                    </div>
                  </div>
                </div>
              ))}

              {/* AI typing indicator */}
              {sendMutation.isPending && (
                <div className="ai-message-row assistant-message">
                  <div className="ai-avatar">
                    <Bot size={20} />
                  </div>

                  <div className="ai-message-content">
                    <span className="ai-message-author">
                      StudyMate AI
                    </span>

                    <div className="ai-typing">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}

              {sendMutation.isError && (
                <div className="ai-error-box">
                  Unable to get an AI response.
                  Please try sending your message again.
                </div>
              )}

              <div ref={messagesEndRef} />

            </div>
          )}

        </div>

        {/* Message input */}
        <div className="ai-input-section">

          <div className="ai-input-box">

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask StudyMate AI anything..."
              rows={2}
              maxLength={10000}
              disabled={
                selectedConversation === null ||
                isBusy
              }
            />

            <button
              className="ai-send-button"
              onClick={handleSendMessage}
              disabled={
                !message.trim() ||
                selectedConversation === null ||
                isBusy
              }
              title="Send message"
            >
              {sendMutation.isPending ? (
                <Loader2 size={19} className="ai-spin" />
              ) : (
                <Send size={19} />
              )}
            </button>

          </div>

          <p>
            Press Enter to send · Shift + Enter for a new line
          </p>

          {createMutation.isError && (
            <div className="ai-error-box">
              Could not create a conversation. Please try again.
            </div>
          )}

          {deleteMutation.isError && (
            <div className="ai-error-box">
              Could not delete the conversation. Please try again.
            </div>
          )}

        </div>

      </main>
    </div>
  );
};

export default AIAssistant;
