
import { useState, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  BookOpen,
  Plus,
  Trash2,
  Pencil,
  Eye,
  EyeOff,
  Layers,
  CheckCircle,
  XCircle,
  ArrowLeft,
} from "lucide-react";

import {
  getFlashcardSets,
  createFlashcardSet,
  updateFlashcardSet,
  deleteFlashcardSet,
  getFlashcards,
  createFlashcard,
  updateFlashcard,
  deleteFlashcard,
  createFlashcardReview,
  type Flashcard,
  type FlashcardSet,
  type FlashcardSetForm,
  type FlashcardForm,
} from "../../services/flashcardService";

import "./Flashcards.css";

export default function Flashcards() {
  const queryClient = useQueryClient();

  const [selectedSet, setSelectedSet] = useState<FlashcardSet | null>(null);
  const [showSetForm, setShowSetForm] = useState(false);
  const [editingSet, setEditingSet] = useState<FlashcardSet | null>(null);
  const [showCardForm, setShowCardForm] = useState(false);
  const [editingCard, setEditingCard] = useState<Flashcard | null>(null);
  const [revealedCards, setRevealedCards] = useState<number[]>([]);

  const [setForm, setSetForm] = useState<FlashcardSetForm>({
    title: "",
    description: "",
  });

  const [cardForm, setCardForm] = useState<FlashcardForm>({
    question: "",
    answer: "",
  });

  const [errorMessage, setErrorMessage] = useState("");

  // Fetch all flashcard sets
  const {
    data: sets = [],
    isLoading: setsLoading,
    isError: setsError,
  } = useQuery({
    queryKey: ["flashcard-sets"],
    queryFn: getFlashcardSets,
  });

  // Fetch cards belonging to the selected set
  const {
    data: cards = [],
    isLoading: cardsLoading,
    isError: cardsError,
  } = useQuery({
    queryKey: ["flashcards", selectedSet?.id],
    queryFn: () => getFlashcards(selectedSet!.id),
    enabled: !!selectedSet,
  });

  const refreshData = () => {
    queryClient.invalidateQueries({ queryKey: ["flashcard-sets"] });
    queryClient.invalidateQueries({ queryKey: ["flashcards"] });
  };

  // Create or update a set
  const setMutation = useMutation({
    mutationFn: (data: FlashcardSetForm) =>
      editingSet
        ? updateFlashcardSet({ id: editingSet.id, data })
        : createFlashcardSet(data),
    onSuccess: (savedSet) => {
      refreshData();
      setShowSetForm(false);
      setEditingSet(null);
      setSetForm({ title: "", description: "" });
      setSelectedSet(savedSet);
      setErrorMessage("");
    },
    onError: () => setErrorMessage("Unable to save the flashcard set."),
  });

  const removeSetMutation = useMutation({
    mutationFn: deleteFlashcardSet,
    onSuccess: () => {
      setSelectedSet(null);
      refreshData();
    },
    onError: () => setErrorMessage("Unable to delete the flashcard set."),
  });

  // Create or update a card
  const cardMutation = useMutation({
    mutationFn: (data: FlashcardForm) =>
      editingCard
        ? updateFlashcard({ id: editingCard.id, data })
        : createFlashcard({ setId: selectedSet!.id, data }),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["flashcards", selectedSet?.id],
      });
      queryClient.invalidateQueries({ queryKey: ["flashcard-sets"] });

      setShowCardForm(false);
      setEditingCard(null);
      setCardForm({ question: "", answer: "" });
      setErrorMessage("");
    },
    onError: () => setErrorMessage("Unable to save the flashcard."),
  });

  const removeCardMutation = useMutation({
    mutationFn: deleteFlashcard,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["flashcards", selectedSet?.id],
      });
      queryClient.invalidateQueries({ queryKey: ["flashcard-sets"] });
    },
    onError: () => setErrorMessage("Unable to delete the flashcard."),
  });

  const reviewMutation = useMutation({
    mutationFn: ({
      flashcardId,
      result,
    }: {
      flashcardId: number;
      result: "known" | "missed";
    }) => createFlashcardReview(flashcardId, result),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flashcard-reviews"] });
      queryClient.invalidateQueries({ queryKey: ["progress-summary"] });
    },
    onError: () => setErrorMessage("Unable to save your review."),
  });

  const handleSetSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");
    setMutation.mutate(setForm);
  };

  const handleCardSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");
    cardMutation.mutate(cardForm);
  };

  const openEditSet = (set: FlashcardSet) => {
    setEditingSet(set);
    setSetForm({
      title: set.title,
      description: set.description,
    });
    setShowSetForm(true);
  };

  const openEditCard = (card: Flashcard) => {
    setEditingCard(card);
    setCardForm({
      question: card.question,
      answer: card.answer,
    });
    setShowCardForm(true);
  };

  const toggleAnswer = (id: number) => {
    setRevealedCards((previous) =>
      previous.includes(id)
        ? previous.filter((cardId) => cardId !== id)
        : [...previous, id]
    );
  };

  const handleReview = (
    card: Flashcard,
    result: "known" | "missed"
  ) => {
    reviewMutation.mutate({
      flashcardId: card.id,
      result,
    });
  };

  if (setsLoading) {
    return <div className="flashcard-message">Loading flashcard sets...</div>;
  }

  if (setsError) {
    return (
      <div className="flashcard-message error">
        Unable to load flashcard sets. Please check your connection.
      </div>
    );
  }

  return (
    <div className="flashcards-page">
      <div className="flashcards-header">
        <div>
          <h1>My Flashcards</h1>
          <p>Create flashcard sets and test your knowledge.</p>
        </div>

        {!selectedSet && (
          <button
            className="flashcard-primary-button"
            onClick={() => {
              setEditingSet(null);
              setSetForm({ title: "", description: "" });
              setShowSetForm(true);
            }}
          >
            <Plus size={18} />
            Create Set
          </button>
        )}
      </div>

      {errorMessage && (
        <div className="flashcard-error">{errorMessage}</div>
      )}

      {/* Set creation and editing */}
      {showSetForm && (
        <form className="flashcard-form" onSubmit={handleSetSubmit}>
          <h2>{editingSet ? "Edit Set" : "Create New Set"}</h2>

          <input
            type="text"
            placeholder="Set title"
            value={setForm.title}
            onChange={(event) =>
              setSetForm({ ...setForm, title: event.target.value })
            }
            required
          />

          <textarea
            placeholder="Description (optional)"
            value={setForm.description}
            onChange={(event) =>
              setSetForm({ ...setForm, description: event.target.value })
            }
          />

          <div className="flashcard-form-actions">
            <button type="submit" disabled={setMutation.isPending}>
              {setMutation.isPending ? "Saving..." : "Save Set"}
            </button>

            <button
              type="button"
              className="flashcard-cancel-button"
              onClick={() => {
                setShowSetForm(false);
                setEditingSet(null);
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Flashcard set list */}
      {!selectedSet && (
        <div className="flashcard-set-grid">
          {sets.length === 0 ? (
            <div className="flashcard-empty">
              <Layers size={42} />
              <h3>No flashcard sets yet</h3>
              <p>Create your first set to start learning.</p>
            </div>
          ) : (
            sets.map((set) => (
              <div className="flashcard-set-card" key={set.id}>
                <div className="flashcard-set-icon">
                  <BookOpen size={25} />
                </div>

                <h3>{set.title}</h3>
                <p>{set.description || "No description added."}</p>
                <span>{set.cards?.length ?? 0} cards</span>

                <div className="flashcard-set-actions">
                  <button onClick={() => setSelectedSet(set)}>
                    Open Set
                  </button>

                  <button
                    title="Edit set"
                    onClick={() => openEditSet(set)}
                  >
                    <Pencil size={17} />
                  </button>

                  <button
                    title="Delete set"
                    onClick={() => {
                      if (
                        window.confirm(
                          `Delete "${set.title}" and all its cards?`
                        )
                      ) {
                        removeSetMutation.mutate(set.id);
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

      {/* Selected set and its cards */}
      {selectedSet && (
        <>
          <div className="flashcard-back-row">
            <button
              onClick={() => {
                setSelectedSet(null);
                setShowCardForm(false);
                setEditingCard(null);
                setRevealedCards([]);
              }}
            >
              <ArrowLeft size={18} />
              All Sets
            </button>
          </div>

          <div className="selected-set-header">
            <div>
              <h2>{selectedSet.title}</h2>
              <p>{selectedSet.description}</p>
            </div>

            <button
              className="flashcard-primary-button"
              onClick={() => {
                setEditingCard(null);
                setCardForm({ question: "", answer: "" });
                setShowCardForm(true);
              }}
            >
              <Plus size={18} />
              Add Card
            </button>
          </div>

          {/* Card form */}
          {showCardForm && (
            <form className="flashcard-form" onSubmit={handleCardSubmit}>
              <h2>{editingCard ? "Edit Card" : "Add New Card"}</h2>

              <textarea
                placeholder="Enter question"
                value={cardForm.question}
                onChange={(event) =>
                  setCardForm({ ...cardForm, question: event.target.value })
                }
                required
              />

              <textarea
                placeholder="Enter answer"
                value={cardForm.answer}
                onChange={(event) =>
                  setCardForm({ ...cardForm, answer: event.target.value })
                }
                required
              />

              <div className="flashcard-form-actions">
                <button type="submit" disabled={cardMutation.isPending}>
                  {cardMutation.isPending ? "Saving..." : "Save Card"}
                </button>

                <button
                  type="button"
                  className="flashcard-cancel-button"
                  onClick={() => {
                    setShowCardForm(false);
                    setEditingCard(null);
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          {cardsLoading ? (
            <p className="flashcard-message">Loading cards...</p>
          ) : cardsError ? (
            <p className="flashcard-message error">Unable to load cards.</p>
          ) : cards.length === 0 ? (
            <div className="flashcard-empty">
              <BookOpen size={42} />
              <h3>No cards in this set</h3>
              <p>Add your first question and answer.</p>
            </div>
          ) : (
            <div className="flashcard-grid">
              {cards.map((card) => {
                const isRevealed = revealedCards.includes(card.id);

                return (
                  <div className="flashcard-item" key={card.id}>
                    <div className="flashcard-item-top">
                      <span>FLASHCARD</span>

                      <div>
                        <button
                          title="Edit card"
                          onClick={() => openEditCard(card)}
                        >
                          <Pencil size={17} />
                        </button>

                        <button
                          title="Delete card"
                          onClick={() => {
                            if (window.confirm("Delete this flashcard?")) {
                              removeCardMutation.mutate(card.id);
                            }
                          }}
                        >
                          <Trash2 size={17} />
                        </button>
                      </div>
                    </div>

                    <h3>{card.question}</h3>

                    {isRevealed && (
                      <div className="flashcard-answer">
                        <strong>Answer</strong>
                        <p>{card.answer}</p>
                      </div>
                    )}

                    <button
                      className="flashcard-reveal-button"
                      onClick={() => toggleAnswer(card.id)}
                    >
                      {isRevealed ? (
                        <>
                          <EyeOff size={17} /> Hide Answer
                        </>
                      ) : (
                        <>
                          <Eye size={17} /> Reveal Answer
                        </>
                      )}
                    </button>

                    {isRevealed && (
                      <div className="flashcard-review-actions">
                        <button
                          className="known-button"
                          disabled={reviewMutation.isPending}
                          onClick={() => handleReview(card, "known")}
                        >
                          <CheckCircle size={17} />
                          Known
                        </button>

                        <button
                          className="missed-button"
                          disabled={reviewMutation.isPending}
                          onClick={() => handleReview(card, "missed")}
                        >
                          <XCircle size={17} />
                          Missed
                        </button>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}
    </div>
  );
}
