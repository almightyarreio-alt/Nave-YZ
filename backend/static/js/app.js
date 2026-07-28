(function () {
    "use strict";

    const elements = {};
    const state = {
        profiles: [],
        flows: [],
        running: false,
        selectedProfile: null,
        activeProfiles: [],
    };

    document.addEventListener("DOMContentLoaded", init);

    async function init() {
        bindElements();
        refreshIcons();
        addLog({ tipo: "info", mensagem: "Dashboard da Central Operacional inicializado." });

        setupEventListeners();

        await Promise.all([
            loadProfiles(),
            loadFlows(),
            loadRuntime(),
        ]);

        // Start periodic runtime update
        setInterval(loadRuntime, 5000);
    }

    function bindElements() {
        elements.profilesList = document.getElementById("profilesList");
        elements.activeProfileDisplay = document.getElementById("activeProfileDisplay");
        elements.flowSelect = document.getElementById("flowSelect");
        elements.runButton = document.getElementById("runButton");
        elements.runButtonText = document.getElementById("runButtonText");
        elements.profileCount = document.getElementById("profileCount");
        elements.flowCount = document.getElementById("flowCount");
        elements.browserCount = document.getElementById("browserCount");
        elements.lastRun = document.getElementById("lastRun");
        elements.timelineLog = document.getElementById("timelineLog");
        elements.statusText = document.getElementById("statusText");

        // Modal Elements
        elements.newProfileBtn = document.getElementById("newProfileBtn");
        elements.newProfileModal = document.getElementById("newProfileModal");
        elements.newProfileNameInput = document.getElementById("newProfileNameInput");
        elements.cancelNewProfileBtn = document.getElementById("cancelNewProfileBtn");
        elements.submitNewProfileBtn = document.getElementById("submitNewProfileBtn");
        elements.modalErrorText = document.getElementById("modalErrorText");
    }

    function setupEventListeners() {
        // Open Modal
        elements.newProfileBtn.addEventListener("click", () => {
            elements.newProfileModal.classList.remove("hidden");
            elements.newProfileModal.classList.add("flex");
            elements.newProfileNameInput.value = "";
            elements.modalErrorText.classList.add("hidden");
            elements.modalErrorText.textContent = "";
            setTimeout(() => elements.newProfileNameInput.focus(), 50);
        });

        // Close Modal
        elements.cancelNewProfileBtn.addEventListener("click", closeModal);
        elements.newProfileModal.addEventListener("click", (e) => {
            if (e.target === elements.newProfileModal) {
                closeModal();
            }
        });

        // Create Profile
        elements.submitNewProfileBtn.addEventListener("click", submitCreateProfile);
        elements.newProfileNameInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                submitCreateProfile();
            }
        });

        // Run automation
        elements.runButton.addEventListener("click", runSelectedFlow);

        // Update run button when flow selection changes
        elements.flowSelect.addEventListener("change", updateRunButton);
    }

    function closeModal() {
        elements.newProfileModal.classList.add("hidden");
        elements.newProfileModal.classList.remove("flex");
        elements.newProfileNameInput.value = "";
        elements.modalErrorText.classList.add("hidden");
        elements.modalErrorText.textContent = "";
    }

    async function submitCreateProfile() {
        const name = elements.newProfileNameInput.value.trim();
        if (!name) {
            showModalError("O nome do perfil é obrigatório.");
            return;
        }

        elements.submitNewProfileBtn.disabled = true;
        elements.submitNewProfileBtn.textContent = "Criando...";

        try {
            const result = await fetchJson("/api/profiles", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name }),
            });

            if (result.logs) {
                result.logs.forEach(addLog);
            }

            closeModal();

            // Auto-select the newly created profile
            const newProfileName = result.profile ? result.profile.name : name;
            state.selectedProfile = newProfileName;

            await loadProfiles();
        } catch (error) {
            showModalError(error.message);
        } finally {
            elements.submitNewProfileBtn.disabled = false;
            elements.submitNewProfileBtn.textContent = "Criar Perfil";
        }
    }

    function showModalError(msg) {
        elements.modalErrorText.textContent = msg;
        elements.modalErrorText.classList.remove("hidden");
    }

    async function loadProfiles() {
        try {
            const profiles = await fetchJson("/api/profiles");
            state.profiles = profiles;

            // Auto-select default profile or first profile if none is currently selected
            if (!state.selectedProfile && profiles.length > 0) {
                const defaultProfile = profiles.find(p => p.default);
                state.selectedProfile = defaultProfile ? defaultProfile.name : profiles[0].name;
            }

            renderProfiles();
            elements.profileCount.textContent = String(state.profiles.length);
        } catch (error) {
            elements.profilesList.innerHTML = `<div class="col-span-2 text-center text-xs text-red-400 py-4 font-mono">Falha ao carregar perfis: ${error.message}</div>`;
            addLog({ tipo: "error", mensagem: `Erro ao carregar perfis: ${error.message}` });
        }
    }

    function renderProfiles() {
        elements.profilesList.replaceChildren();

        if (state.profiles.length === 0) {
            const emptyState = document.createElement("div");
            emptyState.className = "col-span-2 text-center text-xs text-zinc-500 py-8 font-mono";
            emptyState.textContent = "Nenhum perfil cadastrado.";
            elements.profilesList.appendChild(emptyState);

            elements.activeProfileDisplay.textContent = "Nenhum selecionado";
            updateRunButton();
            return;
        }

        // Update selected profile display
        if (state.selectedProfile) {
            elements.activeProfileDisplay.textContent = state.selectedProfile;
        } else {
            elements.activeProfileDisplay.textContent = "Nenhum selecionado";
        }

        state.profiles.forEach(profile => {
            const isSelected = state.selectedProfile === profile.name;
            const card = document.createElement("div");

            card.setAttribute("data-profile-name", profile.name);
            card.className = `flex flex-col justify-between rounded-lg border p-4 transition-all duration-200 cursor-pointer ${
                isSelected
                    ? "border-cyan-500 bg-zinc-900/40 shadow-[0_0_15px_rgba(6,182,212,0.06)]"
                    : "border-zinc-800 bg-zinc-950 hover:border-zinc-700 hover:bg-zinc-900/10"
            }`;
            card.addEventListener("click", () => {
                if (!isSelected) {
                    selectProfile(profile.name);
                }
            });

            // Header info
            const headerDiv = document.createElement("div");
            headerDiv.className = "flex items-start justify-between gap-2";

            const nameElement = document.createElement("h4");
            nameElement.className = "text-sm font-semibold text-white truncate max-w-[70%]";
            nameElement.textContent = profile.name;
            headerDiv.appendChild(nameElement);

            const badgesDiv = document.createElement("div");
            badgesDiv.className = "flex gap-1";

            if (profile.default) {
                const defaultBadge = document.createElement("span");
                defaultBadge.className = "rounded bg-cyan-500/10 border border-cyan-500/30 px-1.5 py-0.5 text-[9px] font-medium text-cyan-300";
                defaultBadge.textContent = "Padrão";
                badgesDiv.appendChild(defaultBadge);
            }

            headerDiv.appendChild(badgesDiv);

            // Body info
            const bodyDiv = document.createElement("div");
            bodyDiv.className = "mt-2 space-y-1.5";

            const statusText = document.createElement("p");
            const isActiveBrowser = state.activeProfiles && state.activeProfiles.includes(profile.name);
            statusText.className = `profile-status text-[11px] font-medium flex items-center gap-1.5 ${
                isActiveBrowser ? "text-emerald-400" : "text-cyan-400/80"
            }`;
            if (isActiveBrowser) {
                statusText.innerHTML = `<span class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Navegador aberto`;
            } else {
                statusText.innerHTML = `<span class="h-1.5 w-1.5 rounded-full bg-cyan-500/50"></span> Persistência ativa`;
            }
            bodyDiv.appendChild(statusText);

            const dirText = document.createElement("p");
            dirText.className = "text-[11px] font-mono text-zinc-500 truncate";
            dirText.textContent = `profiles/${profile.name}`;
            bodyDiv.appendChild(dirText);

            const usageText = document.createElement("p");
            usageText.className = "text-[11px] text-zinc-500";
            usageText.textContent = `Último uso: ${formatLastUsed(profile.last_used)}`;
            bodyDiv.appendChild(usageText);

            // Action buttons
            const actionsDiv = document.createElement("div");
            actionsDiv.className = "mt-4 flex gap-2 border-t border-zinc-900 pt-3";

            // Open Button
            const openBtn = document.createElement("button");
            openBtn.type = "button";
            openBtn.className = "flex-1 h-8 rounded bg-zinc-900 hover:bg-zinc-800 text-xs font-semibold text-zinc-300 transition active:scale-95";
            openBtn.textContent = "Abrir";
            openBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                openProfile(profile.name);
            });
            actionsDiv.appendChild(openBtn);

            // Select Button
            const selectBtn = document.createElement("button");
            selectBtn.type = "button";
            if (isSelected) {
                selectBtn.className = "flex-1 h-8 rounded bg-cyan-500 text-neutral-950 text-xs font-bold transition cursor-default";
                selectBtn.textContent = "Ativo";
            } else {
                selectBtn.className = "flex-1 h-8 rounded border border-zinc-700 hover:border-cyan-500/50 hover:bg-cyan-500/5 text-xs font-semibold text-zinc-400 hover:text-cyan-300 transition active:scale-95";
                selectBtn.textContent = "Selecionar";
                selectBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    selectProfile(profile.name);
                });
            }
            actionsDiv.appendChild(selectBtn);

            // Delete Button
            const deleteBtn = document.createElement("button");
            deleteBtn.type = "button";
            deleteBtn.className = "h-8 w-8 flex items-center justify-center rounded bg-red-950/20 border border-red-500/20 text-red-400 hover:bg-red-950/40 hover:border-red-500/40 transition active:scale-95";
            deleteBtn.title = "Excluir";
            deleteBtn.innerHTML = `<i data-lucide="trash-2" class="h-3.5 w-3.5"></i>`;
            deleteBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                deleteProfile(profile.name);
            });
            actionsDiv.appendChild(deleteBtn);

            card.append(headerDiv, bodyDiv, actionsDiv);
            elements.profilesList.appendChild(card);
        });

        updateRunButton();
        refreshIcons();
    }

    function updateProfileStatuses() {
        state.profiles.forEach(profile => {
            const card = document.querySelector(`[data-profile-name="${CSS.escape(profile.name)}"]`);
            if (!card) return;

            const statusContainer = card.querySelector(".profile-status");
            if (!statusContainer) return;

            const isActive = state.activeProfiles.includes(profile.name);
            if (isActive) {
                statusContainer.className = "profile-status text-[11px] font-medium text-emerald-400 flex items-center gap-1.5";
                statusContainer.innerHTML = `<span class="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Navegador aberto`;
            } else {
                statusContainer.className = "profile-status text-[11px] font-medium text-cyan-400/80 flex items-center gap-1.5";
                statusContainer.innerHTML = `<span class="h-1.5 w-1.5 rounded-full bg-cyan-500/50"></span> Persistência ativa`;
            }
        });
    }

    async function selectProfile(name) {
        state.selectedProfile = name;
        elements.activeProfileDisplay.textContent = name;
        updateRunButton();

        try {
            await fetchJson("/api/profiles/default", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name }),
            });
            await loadProfiles();
        } catch (error) {
            addLog({ tipo: "warning", mensagem: `Erro ao definir perfil padrão no backend: ${error.message}` });
            renderProfiles();
        }
    }

    async function openProfile(name) {
        addLog({ tipo: "info", mensagem: `Abrindo navegador do perfil: ${name}...` });
        try {
            const result = await fetchJson("/api/profiles/open", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name }),
            });

            if (result.logs) {
                result.logs.forEach(addLog);
            }
            updateRuntime(result);
            addLog({ tipo: "success", mensagem: `Navegador do perfil "${name}" carregado.` });
        } catch (error) {
            addLog({ tipo: "error", mensagem: `Falha ao abrir o perfil: ${error.message}` });
        }
    }

    async function deleteProfile(name) {
        const confirmed = confirm(`Deseja realmente excluir o perfil "${name}"?\nEsta ação apagará permanentemente todos os dados de navegação persistidos.`);
        if (!confirmed) return;

        addLog({ tipo: "info", mensagem: `Removendo perfil: ${name}...` });
        try {
            const result = await fetchJson(`/api/profiles/${encodeURIComponent(name)}`, {
                method: "DELETE",
            });

            if (result.logs) {
                result.logs.forEach(addLog);
            }

            if (state.selectedProfile === name) {
                state.selectedProfile = null;
            }

            addLog({ tipo: "success", mensagem: `Perfil "${name}" removido com sucesso.` });
            await loadProfiles();
        } catch (error) {
            addLog({ tipo: "error", mensagem: `Falha ao remover perfil: ${error.message}` });
        }
    }

    async function loadFlows() {
        try {
            state.flows = await fetchJson("/api/flows");
            populateSelect(elements.flowSelect, state.flows, "Nenhum fluxo encontrado");
            elements.flowCount.textContent = String(state.flows.length);
        } catch (error) {
            populateSelect(elements.flowSelect, [], "Falha ao carregar fluxos");
            addLog({ tipo: "error", mensagem: error.message });
        }
    }

    async function loadRuntime() {
        try {
            const runtime = await fetchJson("/api/runtime");
            updateRuntime(runtime);
        } catch (error) {
            // Silently swallow periodic runtime request errors to avoid spamming the log.
        }
    }

    async function runSelectedFlow() {
        const profile = state.selectedProfile;
        const flow = elements.flowSelect.value;

        if (!profile || !flow) {
            addLog({ tipo: "warning", mensagem: "Selecione um perfil ativo e um fluxo." });
            return;
        }

        setRunning(true);
        addLog({ tipo: "info", mensagem: `Iniciando automação com o fluxo "${flow}" no perfil "${profile}"...` });

        try {
            const result = await fetchJson("/api/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ profile, flow }),
            });

            if (Array.isArray(result.logs)) {
                result.logs.forEach(addLog);
            }
            updateRuntime(result);
            addLog({ tipo: "success", mensagem: `Fluxo "${flow}" finalizado.` });
        } catch (error) {
            addLog({ tipo: "error", mensagem: error.message });
        } finally {
            setRunning(false);
        }
    }

    function populateSelect(select, items, emptyText) {
        select.replaceChildren();

        if (!items.length) {
            const option = document.createElement("option");
            option.value = "";
            option.textContent = emptyText;
            select.appendChild(option);
            return;
        }

        // Default empty option
        const placeholderOption = document.createElement("option");
        placeholderOption.value = "";
        placeholderOption.textContent = "-- Selecione um fluxo --";
        select.appendChild(placeholderOption);

        items.forEach((item) => {
            const option = document.createElement("option");
            option.value = item;
            option.textContent = item;
            select.appendChild(option);
        });
    }

    async function fetchJson(url, options) {
        const response = await fetch(url, options);
        const contentType = response.headers.get("content-type") || "";
        const payload = contentType.includes("application/json")
            ? await response.json()
            : await response.text();

        if (!response.ok) {
            const message = typeof payload === "string"
                ? payload
                : payload.detail || "Erro inesperado na API.";
            throw new Error(message);
        }

        return payload;
    }

    function updateRuntime(runtime) {
        if (typeof runtime.active_browsers === "number") {
            elements.browserCount.textContent = String(runtime.active_browsers);
        }

        if (runtime.last_execution) {
            const execution = runtime.last_execution;
            elements.lastRun.textContent = `${execution.flow || "Fluxo"} - ${execution.finished_at || ""}`;
            elements.lastRun.title = elements.lastRun.textContent;
        }

        if (runtime.pages) {
            state.activeProfiles = runtime.pages.map(p => p.profile);
            updateProfileStatuses();
        }
    }

    function updateRunButton() {
        const disabled = state.running || !state.selectedProfile || !elements.flowSelect.value;
        elements.runButton.disabled = disabled;
    }

    function setRunning(isRunning) {
        state.running = isRunning;

        // Update status badge in header
        const statusBadge = document.getElementById("statusBadge");
        const statusIndicator = document.getElementById("statusIndicator");
        const statusText = document.getElementById("statusText");

        if (statusText) {
            statusText.textContent = isRunning ? "Executando" : "Motor local";
        }

        if (statusBadge && statusIndicator) {
            if (isRunning) {
                statusBadge.className = "flex items-center gap-2 rounded-lg border border-cyan-500/20 bg-cyan-500/10 px-3 py-2 text-xs text-cyan-300 font-semibold";
                statusIndicator.innerHTML = `
                    <span class="absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75 animate-ping"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
                `;
            } else {
                statusBadge.className = "flex items-center gap-2 rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-3 py-2 text-xs text-emerald-300";
                statusIndicator.innerHTML = `
                    <span class="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                `;
            }
        }

        // Update runtime status badge
        const runtimeBadge = document.getElementById("runtimeBadge");
        if (runtimeBadge) {
            if (isRunning) {
                runtimeBadge.className = "flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-300 font-semibold font-mono";
                runtimeBadge.innerHTML = `
                    <span class="relative flex h-2 w-2">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span> EXECUTANDO
                `;
            } else {
                runtimeBadge.className = "flex items-center gap-2 rounded-full border border-zinc-800 bg-zinc-900/50 px-3 py-1 text-xs text-zinc-400 font-mono";
                runtimeBadge.innerHTML = `<span class="h-2 w-2 rounded-full bg-zinc-600"></span> IDLE`;
            }
        }

        if (isRunning) {
            elements.runButton.disabled = true;
            elements.runButtonText.textContent = "Executando...";
            // Insert spinner SVG
            const spinner = document.createElement("span");
            spinner.id = "runSpinner";
            spinner.innerHTML = `
                <svg class="animate-spin h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            `;
            // Remove the play icon if it's there
            const existingIcon = elements.runButton.querySelector("i");
            if (existingIcon) {
                existingIcon.classList.add("hidden");
            }
            // Prepend spinner
            elements.runButton.insertBefore(spinner, elements.runButtonText);
            elements.flowSelect.disabled = true;
        } else {
            elements.runButtonText.textContent = "Executar Automação";
            const spinner = document.getElementById("runSpinner");
            if (spinner) {
                spinner.remove();
            }
            const existingIcon = elements.runButton.querySelector("i");
            if (existingIcon) {
                existingIcon.classList.remove("hidden");
            }
            elements.flowSelect.disabled = false;
        }

        updateRunButton();
    }

    function formatLogTime(timestampStr) {
        if (!timestampStr) {
            return new Date().toLocaleTimeString("pt-BR");
        }
        try {
            if (timestampStr.includes("T")) {
                const parts = timestampStr.split("T");
                if (parts[1]) {
                    return parts[1].split(".")[0];
                }
            }
            if (timestampStr.includes(",")) {
                return timestampStr.split(",")[1].trim();
            }
            return timestampStr;
        } catch (e) {
            return timestampStr;
        }
    }

    function addLog(entry) {
        const row = document.createElement("div");
        row.className = "grid grid-cols-[5.5rem_4.5rem_minmax(0,1fr)] gap-2 border-b border-zinc-900/50 py-1 text-xs font-mono items-center animate-fade-in";

        const timestamp = document.createElement("span");
        timestamp.className = "text-[11px] text-zinc-500";
        timestamp.textContent = formatLogTime(entry.timestamp);

        const type = document.createElement("span");
        type.className = `w-fit rounded border px-1 py-0.5 text-[9px] uppercase font-bold tracking-wider ${typeClass(entry.tipo)}`;
        type.textContent = entry.tipo || "info";

        const message = document.createElement("span");
        message.className = "min-w-0 break-words text-zinc-300";
        message.textContent = entry.mensagem || "";

        row.append(timestamp, type, message);
        elements.timelineLog.appendChild(row);

        // Auto-scroll
        const container = elements.timelineLog;
        const threshold = 60; // px
        const isNearBottom = (container.scrollHeight - container.clientHeight) - container.scrollTop < threshold;
        if (isNearBottom || container.children.length === 1) {
            container.scrollTop = container.scrollHeight;
        }
    }

    function typeClass(type) {
        const classes = {
            success: "border-emerald-500/20 bg-emerald-500/5 text-emerald-400",
            error: "border-rose-500/20 bg-rose-500/5 text-rose-400",
            warning: "border-amber-500/20 bg-amber-500/5 text-amber-400",
            info: "border-cyan-500/20 bg-cyan-500/5 text-cyan-400",
        };
        return classes[type] || classes.info;
    }

    function formatLastUsed(isoStr) {
        if (!isoStr) return "Nunca";
        try {
            const date = new Date(isoStr);
            if (isNaN(date.getTime())) return isoStr;

            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            const diffHours = Math.floor(diffMins / 60);
            const diffDays = Math.floor(diffHours / 24);

            if (diffMins < 1) return "agora mesmo";
            if (diffMins < 60) return `há ${diffMins} min`;
            if (diffHours < 24) {
                if (now.getDate() === date.getDate()) {
                    return `hoje às ${date.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
                }
                return `ontem às ${date.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
            }
            if (diffDays === 1) return `ontem às ${date.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
            return date.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
        } catch (e) {
            return isoStr;
        }
    }

    function refreshIcons() {
        if (window.lucide && typeof window.lucide.createIcons === "function") {
            window.lucide.createIcons();
        }
    }
})();
