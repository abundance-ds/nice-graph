<script setup lang="ts">
import { marked } from "marked";

const route = useRoute();
const router = useRouter();

const question = ref((route.query.q as string) || "");
const loading = ref(false);
const error = ref("");
const bottomRef = ref<HTMLElement | null>(null);
const userScrolledUp = ref(false);

const token = computed(() => (route.query.token as string) || "");
const isAuthed = computed(() => !!token.value);

interface Turn {
  role: "user" | "assistant";
  question?: string;
  answer?: string;
  queries?: { sql: string; rows: any[]; error?: string }[];
  status?: string;
}

const conversation = ref<Turn[]>([]);

const assistantTurns = computed(
  () => conversation.value.filter((t) => t.role === "assistant").length
);
const maxTurns = 5;
const limitReached = computed(() => !isAuthed.value && assistantTurns.value >= maxTurns);

const apiHistory = computed(() => {
  const msgs: { role: string; content: string }[] = [];
  for (const turn of conversation.value) {
    if (turn.role === "user" && turn.question)
      msgs.push({ role: "user", content: turn.question });
    if (turn.role === "assistant" && turn.answer)
      msgs.push({ role: "assistant", content: turn.answer });
  }
  return msgs;
});

async function ask() {
  if (!question.value.trim() || loading.value || limitReached.value) return;

  const q = question.value;
  question.value = "";
  loading.value = true;
  error.value = "";

  if (conversation.value.length === 0) {
    router.replace({ query: { q, ...(token.value ? { token: token.value } : {}) } });
  }

  conversation.value.push({ role: "user", question: q });
  conversation.value.push({
    role: "assistant",
    answer: "",
    queries: [],
    status: "",
  });
  const turnIndex = conversation.value.length - 1;

  await nextTick();
  scrollToBottom();

  try {
    userScrolledUp.value = false;
    const historyToSend = apiHistory.value.slice(0, -1);
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, history: historyToSend, token: token.value || undefined }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let lastScroll = 0;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";

      for (const part of parts) {
        const dataLine = part
          .split("\n")
          .find((l) => l.startsWith("data: "));
        if (!dataLine) continue;
        try {
          const data = JSON.parse(dataLine.slice(6));
          const turn = conversation.value[turnIndex];

          if (data.type === "text") {
            turn.answer = (turn.answer || "") + data.text;
            turn.status = "";
            const now = Date.now();
            if (now - lastScroll > 200) {
              lastScroll = now;
              scrollToBottom();
            }
          } else if (data.type === "query") {
            turn.queries = [
              ...(turn.queries || []),
              { sql: data.sql, rows: data.rows, error: data.error },
            ];
          } else if (data.type === "status") {
            turn.status = data.message;
            scrollToBottom();
          } else if (data.type === "error") {
            error.value = data.message;
          }
        } catch {
          // skip malformed events
        }
      }
    }
  } catch (e: any) {
    error.value = e.message || "Something went wrong";
  } finally {
    if (conversation.value[turnIndex]) {
      conversation.value[turnIndex].status = "";
    }
    loading.value = false;
    await nextTick();
    scrollToBottom();
  }
}

function newConversation() {
  conversation.value = [];
  question.value = "";
  error.value = "";
  router.replace({ query: token.value ? { token: token.value } : {} });
}

function scrollToBottom() {
  if (userScrolledUp.value) return;
  nextTick(() => {
    bottomRef.value?.scrollIntoView({ behavior: "smooth" });
  });
}

function onScroll() {
  if (!loading.value) return;
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const windowHeight = window.innerHeight;
  const docHeight = document.documentElement.scrollHeight;
  const distFromBottom = docHeight - scrollTop - windowHeight;
  if (distFromBottom > 400) {
    userScrolledUp.value = true;
  } else if (distFromBottom < 100) {
    userScrolledUp.value = false;
  }
}

function renderMarkdown(text: string): string {
  if (!text) return "";
  let html = marked.parse(text, { async: false }) as string;
  html = html.replace(
    /\bTA(\d+)\b/g,
    '<a href="/ta/$1" class="text-stone-900 font-medium hover:text-cadet-600 transition-colors underline decoration-stone-200 underline-offset-2">TA$1</a>'
  );
  return html;
}

function formatRows(rows: any[]): string {
  if (!rows.length) return "No rows returned.";
  const display = rows.slice(0, 15);
  const json = JSON.stringify(display, null, 2);
  if (rows.length > 15) return json + `\n... (${rows.length} total rows)`;
  return json;
}

onMounted(() => {
  window.addEventListener("scroll", onScroll, { passive: true });
  if (route.query.q) {
    question.value = route.query.q as string;
    ask();
  }
});

onUnmounted(() => {
  window.removeEventListener("scroll", onScroll);
});
</script>

<template>
  <div
    class="flex flex-col"
    :class="conversation.length ? 'min-h-[calc(100vh-128px)]' : 'min-h-[calc(100vh-128px)]'"
  >
    <!-- Header (only before conversation starts) -->
    <div v-if="!conversation.length" class="py-16 px-6">
      <div class="max-w-3xl mx-auto">
        <div class="flex items-center gap-3 mb-4">
          <p
            class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em]"
          >
            Ask
          </p>
          <span v-if="isAuthed" class="text-[10px] font-semibold uppercase tracking-[0.12em] text-stone-400 border border-stone-200 rounded px-1.5 py-0.5">Pro</span>
        </div>
        <h1
          class="text-2xl md:text-3xl font-serif font-semibold leading-tight tracking-tight text-stone-900"
        >
          Query the knowledge graph
        </h1>
        <p class="mt-3 text-sm text-stone-400">
          Natural language questions answered by AI. Follow-up questions
          supported.
        </p>
      </div>
    </div>

    <!-- Conversation thread -->
    <div v-if="conversation.length" class="flex-1 px-6 pt-6 pb-36">
      <div class="max-w-3xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <p
              class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em]"
            >
              Ask
            </p>
            <span v-if="isAuthed" class="text-[10px] font-semibold uppercase tracking-[0.12em] text-stone-400 border border-stone-200 rounded px-1.5 py-0.5">Pro</span>
          </div>
          <button
            @click="newConversation"
            class="text-xs text-stone-400 hover:text-stone-600 transition-colors"
          >
            New conversation
          </button>
        </div>

        <div class="space-y-6">
          <template v-for="(turn, i) in conversation" :key="i">
            <div
              v-if="turn.role === 'user'"
              class="pt-4 flex justify-end"
              :class="{ 'border-t border-stone-100': i > 0 }"
            >
              <p class="text-base font-medium text-stone-900 bg-stone-50 rounded-2xl rounded-br-sm px-4 py-2.5 max-w-[75%]">
                {{ turn.question }}
              </p>
            </div>

            <div v-if="turn.role === 'assistant'" class="mt-3">
              <!-- Status (querying database...) -->
              <div
                v-if="turn.status"
                class="flex items-center gap-2 text-sm text-stone-400 py-2"
              >
                <span
                  class="w-1.5 h-1.5 bg-stone-300 rounded-full animate-pulse"
                ></span>
                {{ turn.status }}
              </div>

              <!-- Streaming text -->
              <div
                v-if="turn.answer"
                class="prose prose-stone max-w-none prose-sm prose-headings:font-serif prose-headings:font-semibold prose-headings:tracking-tight prose-p:text-stone-600 prose-p:leading-relaxed prose-li:text-stone-600 prose-strong:text-stone-900 prose-table:text-sm prose-th:text-left prose-th:font-semibold prose-th:text-stone-900 prose-td:py-1 prose-td:pr-4 prose-th:py-1 prose-th:pr-4 prose-td:border-stone-100 prose-th:border-stone-200 prose-a:text-stone-900 prose-a:font-medium prose-a:no-underline hover:prose-a:text-cadet-600"
                v-html="renderMarkdown(turn.answer)"
              />

              <!-- Loading dots (no text yet and still loading) -->
              <div
                v-if="!turn.answer && !turn.status && loading && i === conversation.length - 1"
                class="flex gap-1.5 py-2"
              >
                <span
                  class="w-1.5 h-1.5 bg-stone-300 rounded-full animate-bounce"
                  style="animation-delay: 0ms"
                ></span>
                <span
                  class="w-1.5 h-1.5 bg-stone-300 rounded-full animate-bounce"
                  style="animation-delay: 150ms"
                ></span>
                <span
                  class="w-1.5 h-1.5 bg-stone-300 rounded-full animate-bounce"
                  style="animation-delay: 300ms"
                ></span>
              </div>

              <!-- Queries (collapsed) -->
              <details
                v-if="turn.queries?.length"
                class="mt-4 text-xs text-stone-300"
              >
                <summary
                  class="cursor-pointer hover:text-stone-400 transition-colors"
                >
                  {{ turn.queries.length }}
                  {{ turn.queries.length === 1 ? "query" : "queries" }}
                  executed
                </summary>
                <div class="mt-2 space-y-4">
                  <div v-for="(q, j) in turn.queries" :key="j">
                    <pre
                      class="bg-stone-50 rounded p-3 overflow-x-auto text-stone-500 font-mono text-xs"
                    >{{ q.sql }}</pre>
                    <p class="mt-1 text-stone-300">
                      {{ q.rows.length }} row{{
                        q.rows.length === 1 ? "" : "s"
                      }}
                    </p>
                    <details class="mt-1">
                      <summary
                        class="cursor-pointer hover:text-stone-400 transition-colors"
                      >
                        Raw results
                      </summary>
                      <pre
                        class="mt-1 bg-stone-50 rounded p-3 overflow-x-auto text-stone-400 font-mono text-xs max-h-64 overflow-y-auto"
                      >{{ formatRows(q.rows) }}</pre>
                    </details>
                  </div>
                </div>
              </details>
            </div>
          </template>

          <!-- Error -->
          <div v-if="error" class="pt-4">
            <p class="text-sm text-stone-600">{{ error }}</p>
          </div>

          <!-- Turn limit -->
          <div v-if="limitReached" class="pt-4 border-t border-stone-100">
            <p class="text-sm text-stone-400">
              Conversation limit reached ({{ maxTurns }} turns).
              <button
                @click="newConversation"
                class="text-stone-600 hover:text-stone-900 underline transition-colors"
              >
                Start a new conversation
              </button>
            </p>
          </div>
        </div>

        <div ref="bottomRef" />
      </div>
    </div>

    <!-- Input area -->
    <div
      :class="
        conversation.length
          ? 'fixed bottom-0 left-0 right-0 bg-white border-t border-stone-100 px-6 py-4 z-10'
          : 'px-6'
      "
    >
      <div class="max-w-3xl mx-auto">
        <form @submit.prevent="ask">
          <div
            class="flex items-center border border-stone-200 rounded px-4 py-3 focus-within:border-stone-400 transition-colors"
          >
            <input
              v-model="question"
              type="text"
              :placeholder="
                conversation.length
                  ? 'Ask a follow-up...'
                  : 'What survival extrapolation methods has NICE accepted for lung cancer?'
              "
              class="flex-1 text-base text-stone-900 placeholder:text-stone-300 outline-none bg-transparent"
              :disabled="loading || limitReached"
            />
            <button
              type="submit"
              :disabled="loading || limitReached"
              class="ml-3 px-5 py-2 text-sm font-medium bg-stone-900 hover:bg-stone-800 text-white rounded tracking-wide transition-colors disabled:opacity-50"
            >
              {{ loading ? "..." : "Send" }}
            </button>
          </div>
        </form>
        <p class="mt-2 text-xs text-stone-300 text-center">
          Experimental. Answers are AI-generated and may be inaccurate.
        </p>
      </div>
    </div>
  </div>
</template>
