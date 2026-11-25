
import { useState, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Plus,
  Trash2,
  ArrowLeft,
  BookOpen,
  CheckCircle,
  Trophy,
  ClipboardList,
} from "lucide-react";

import {
  getQuizzes,
  createQuiz,
  deleteQuiz,
  getQuizDetails,
  createQuestion,
  createQuizOption,
  submitQuiz,
  getQuizAttempts,
  type Quiz,
  type QuizDetails,
  type QuizSubmissionResult,
} from "../../services/quizService";

import "./Quizzes.css";

type SelectedAnswers = Record<number, number | null>;

export default function Quizzes() {
  const queryClient = useQueryClient();

  const [selectedQuiz, setSelectedQuiz] = useState<Quiz | null>(null);
  const [mode, setMode] = useState<"manage" | "take" | "result" | "history">("manage");

  const [showQuizForm, setShowQuizForm] = useState(false);
  const [quizTitle, setQuizTitle] = useState("");
  const [quizDescription, setQuizDescription] = useState("");

  const [questionText, setQuestionText] = useState("");
  const [questionMarks, setQuestionMarks] = useState(1);

  const [optionTexts, setOptionTexts] = useState(["", "", "", ""]);
  const [correctOption, setCorrectOption] = useState(0);

  const [selectedAnswers, setSelectedAnswers] = useState<SelectedAnswers>({});
  const [result, setResult] = useState<QuizSubmissionResult | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  const { data: quizzes = [], isLoading, isError } = useQuery({
    queryKey: ["quizzes"],
    queryFn: getQuizzes,
  });

  const {
    data: quizDetails,
    isLoading: detailsLoading,
    refetch: refreshDetails,
  } = useQuery({
    queryKey: ["quiz-details", selectedQuiz?.id],
    queryFn: () => getQuizDetails(selectedQuiz!.id),
    enabled: !!selectedQuiz,
  });

  const { data: attempts = [] } = useQuery({
    queryKey: ["quiz-attempts", selectedQuiz?.id],
    queryFn: () => getQuizAttempts(selectedQuiz?.id),
    enabled: !!selectedQuiz && mode === "history",
  });

  const quizMutation = useMutation({
    mutationFn: createQuiz,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["quizzes"] });
      setQuizTitle("");
      setQuizDescription("");
      setShowQuizForm(false);
      setErrorMessage("");
    },
    onError: () => setErrorMessage("Unable to create quiz."),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteQuiz,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["quizzes"] });
      setSelectedQuiz(null);
    },
    onError: () => setErrorMessage("Unable to delete quiz."),
  });

  const questionMutation = useMutation({
    mutationFn: createQuestion,
    onSuccess: async (question) => {
      try {
        const optionRequests = optionTexts
          .map((text, index) => ({ text: text.trim(), index }))
          .filter((option) => option.text)
          .map((option) =>
            createQuizOption({
              questionId: question.id,
              data: {
                option_text: option.text,
                is_correct: option.index === correctOption,
              },
            })
          );

        await Promise.all(optionRequests);

        setQuestionText("");
        setQuestionMarks(1);
        setOptionTexts(["", "", "", ""]);
        setCorrectOption(0);
        setErrorMessage("");

        await refreshDetails();
      } catch {
        setErrorMessage(
          "The question was created, but one or more options could not be saved. Please check the quiz."
        );
        await refreshDetails();
      }
    },
    onError: () => setErrorMessage("Unable to create question."),
  });

  const submissionMutation = useMutation({
    mutationFn: submitQuiz,
    onSuccess: (data) => {
      setResult(data);
      setMode("result");
      queryClient.invalidateQueries({ queryKey: ["quiz-attempts"] });
      queryClient.invalidateQueries({ queryKey: ["progress-summary"] });
    },
    onError: () => setErrorMessage("Unable to submit quiz."),
  });

  const handleQuizSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");
    quizMutation.mutate({
      title: quizTitle,
      description: quizDescription,
    });
  };

  const handleQuestionSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedQuiz) return;

    if (optionTexts.filter((option) => option.trim()).length < 2) {
      setErrorMessage("Please enter at least two options.");
      return;
    }

    if (!optionTexts[correctOption]?.trim()) {
      setErrorMessage("Please enter text for the correct option.");
      return;
    }

    setErrorMessage("");

    questionMutation.mutate({
      quizId: selectedQuiz.id,
      data: {
        question_text: questionText,
        marks: questionMarks,
      },
    });
  };

  const handleStartQuiz = () => {
    if (!quizDetails?.questions.length) {
      setErrorMessage("Add questions before taking this quiz.");
      return;
    }

    setSelectedAnswers({});
    setResult(null);
    setErrorMessage("");
    setMode("take");
  };

  const handleSubmitAnswers = () => {
    if (!selectedQuiz || !quizDetails) return;

    const answers = quizDetails.questions.map((question) => ({
      question: question.id,
      selected_option: selectedAnswers[question.id] ?? null,
    }));

    submissionMutation.mutate({
      quizId: selectedQuiz.id,
      data: { answers },
    });
  };

  const openQuiz = (quiz: Quiz) => {
    setSelectedQuiz(quiz);
    setMode("manage");
    setErrorMessage("");
  };

  const goBack = () => {
    setSelectedQuiz(null);
    setMode("manage");
    setResult(null);
    setErrorMessage("");
  };

  if (isLoading) {
    return <div className="quiz-message">Loading quizzes...</div>;
  }

  if (isError) {
    return <div className="quiz-message quiz-error">Unable to load quizzes.</div>;
  }

  return (
    <div className="quizzes-page">
      <div className="quizzes-header">
        <div>
          <h1>My Quizzes</h1>
          <p>Create quizzes, test your knowledge and track your scores.</p>
        </div>

        {!selectedQuiz && (
          <button
            className="quiz-primary-button"
            onClick={() => setShowQuizForm(true)}
          >
            <Plus size={18} />
            Create Quiz
          </button>
        )}
      </div>

      {errorMessage && <div className="quiz-error-box">{errorMessage}</div>}

      {/* Create quiz */}
      {!selectedQuiz && showQuizForm && (
        <form className="quiz-form" onSubmit={handleQuizSubmit}>
          <h2>Create a Quiz</h2>

          <input
            value={quizTitle}
            onChange={(event) => setQuizTitle(event.target.value)}
            placeholder="Quiz title"
            required
          />

          <textarea
            value={quizDescription}
            onChange={(event) => setQuizDescription(event.target.value)}
            placeholder="Quiz description"
          />

          <div className="quiz-form-actions">
            <button type="submit" disabled={quizMutation.isPending}>
              {quizMutation.isPending ? "Creating..." : "Create"}
            </button>

            <button
              type="button"
              className="quiz-secondary-button"
              onClick={() => setShowQuizForm(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Quiz list */}
      {!selectedQuiz && (
        <div className="quiz-grid">
          {quizzes.length === 0 ? (
            <div className="quiz-empty">
              <ClipboardList size={42} />
              <h3>No quizzes created yet</h3>
              <p>Create your first quiz to get started.</p>
            </div>
          ) : (
            quizzes.map((quiz) => (
              <div className="quiz-card" key={quiz.id}>
                <div className="quiz-card-icon">
                  <BookOpen size={25} />
                </div>

                <h3>{quiz.title}</h3>
                <p>{quiz.description || "No description added."}</p>

                <span>{quiz.question_count} questions</span>

                <div className="quiz-card-actions">
                  <button onClick={() => openQuiz(quiz)}>
                    Open Quiz
                  </button>

                  <button
                    title="Delete quiz"
                    onClick={() => {
                      if (window.confirm(`Delete "${quiz.title}"?`)) {
                        deleteMutation.mutate(quiz.id);
                      }
                    }}
                  >
                    <Trash2 size={17} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Selected quiz */}
      {selectedQuiz && (
        <>
          <button className="quiz-back-button" onClick={goBack}>
            <ArrowLeft size={18} /> All Quizzes
          </button>

          <div className="quiz-detail-header">
            <div>
              <h2>{selectedQuiz.title}</h2>
              <p>{selectedQuiz.description}</p>
            </div>

            {mode === "manage" && (
              <div className="quiz-detail-actions">
                <button
                  className="quiz-secondary-button"
                  onClick={() => setMode("history")}
                >
                  <ClipboardList size={17} /> Attempts
                </button>

                <button
                  className="quiz-primary-button"
                  onClick={handleStartQuiz}
                >
                  <Trophy size={17} /> Take Quiz
                </button>
              </div>
            )}
          </div>

          {detailsLoading ? (
            <p className="quiz-message">Loading quiz questions...</p>
          ) : (
            <>
              {/* Manage questions */}
              {mode === "manage" && (
                <>
                  <form className="quiz-form" onSubmit={handleQuestionSubmit}>
                    <h3>Add a Question</h3>

                    <textarea
                      value={questionText}
                      onChange={(event) => setQuestionText(event.target.value)}
                      placeholder="Enter your question"
                      required
                    />

                    <label>Marks</label>
                    <input
                      type="number"
                      min="1"
                      value={questionMarks}
                      onChange={(event) =>
                        setQuestionMarks(Number(event.target.value))
                      }
                      required
                    />

                    <h4>Options</h4>

                    {optionTexts.map((option, index) => (
                      <div className="quiz-option-editor" key={index}>
                        <input
                          value={option}
                          onChange={(event) => {
                            const updated = [...optionTexts];
                            updated[index] = event.target.value;
                            setOptionTexts(updated);
                          }}
                          placeholder={`Option ${index + 1}`}
                        />

                        <label>
                          <input
                            type="radio"
                            name="correct-option"
                            checked={correctOption === index}
                            onChange={() => setCorrectOption(index)}
                          />
                          Correct
                        </label>
                      </div>
                    ))}

                    <button
                      type="submit"
                      disabled={questionMutation.isPending}
                    >
                      {questionMutation.isPending
                        ? "Saving..."
                        : "Add Question and Options"}
                    </button>
                  </form>

                  <h3 className="quiz-section-title">
                    Questions ({quizDetails?.questions.length ?? 0})
                  </h3>

                  {quizDetails?.questions.map((question, index) => (
                    <div className="quiz-question-card" key={question.id}>
                      <strong>
                        {index + 1}. {question.question_text}
                      </strong>

                      <span>{question.marks} marks</span>

                      <ul>
                        {question.options.map((option) => (
                          <li key={option.id}>{option.option_text}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </>
              )}

              {/* Take quiz */}
              {mode === "take" && (
                <div className="take-quiz-section">
                  <h3>Answer the questions</h3>

                  {quizDetails?.questions.map((question, index) => (
                    <div className="quiz-question-card" key={question.id}>
                      <strong>
                        {index + 1}. {question.question_text}
                      </strong>

                      <span>{question.marks} marks</span>

                      {question.options.map((option) => (
                        <label className="quiz-answer-option" key={option.id}>
                          <input
                            type="radio"
                            name={`question-${question.id}`}
                            checked={selectedAnswers[question.id] === option.id}
                            onChange={() =>
                              setSelectedAnswers((previous) => ({
                                ...previous,
                                [question.id]: option.id,
                              }))
                            }
                          />
                          {option.option_text}
                        </label>
                      ))}
                    </div>
                  ))}

                  <button
                    className="quiz-primary-button"
                    disabled={submissionMutation.isPending}
                    onClick={handleSubmitAnswers}
                  >
                    {submissionMutation.isPending
                      ? "Submitting..."
                      : "Submit Quiz"}
                  </button>
                </div>
              )}

              {/* Result */}
              {mode === "result" && result && (
                <div className="quiz-result-card">
                  <Trophy size={42} />
                  <h2>Quiz Completed!</h2>

                  <div className="quiz-score">
                    {result.percentage}%
                  </div>

                  <p>
                    Score: {result.score} / {result.total_marks}
                  </p>

                  <div className="quiz-result-stats">
                    <div>
                      <strong>{result.correct_answers}</strong>
                      <span>Correct</span>
                    </div>

                    <div>
                      <strong>{result.total_questions}</strong>
                      <span>Total Questions</span>
                    </div>
                  </div>

                  <button
                    className="quiz-primary-button"
                    onClick={() => setMode("manage")}
                  >
                    Back to Quiz
                  </button>
                </div>
              )}

              {/* Attempt history */}
              {mode === "history" && (
                <div className="quiz-history">
                  <h3>Quiz Attempts</h3>

                  {attempts.length === 0 ? (
                    <p>No attempts recorded yet.</p>
                  ) : (
                    attempts.map((attempt) => (
                      <div className="quiz-attempt-row" key={attempt.id}>
                        <div>
                          <strong>
                            {attempt.score} / {attempt.total_marks}
                          </strong>
                          <p>
                            {new Date(attempt.submitted_at).toLocaleString()}
                          </p>
                        </div>
                        <CheckCircle size={20} />
                      </div>
                    ))
                  )}

                  <button
                    className="quiz-secondary-button"
                    onClick={() => setMode("manage")}
                  >
                    Back
                  </button>
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  );
}
