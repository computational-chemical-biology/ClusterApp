import { dropzoneManager } from "./dropzone/DropzoneManager.js";
const FILE_PATH = '/static/csv/example_file_clusterapp.csv';

async function prefillForm(formId) {
    const form = document.getElementById(formId);
    if (!form) {
        console.error(`Formulário com ID '${formId}' não encontrado.`);
        return;
    }

    const values = getPrefillValues(formId);
    fillFormInputs(form, values, formId);
    await autoFillCsv(formId);
}


function getPrefillValues(formId) {
    if (formId === 'clustering-form') {
        return {
            taskid: "c66bf306c305449e856edc355e61ab20",
            workflow: "FBMN-gnps2",
            metric: "canberra",
            normalization: "",
            scaling: "",
            shared: true,
            prop_blank_feats: 0.5,
            prop_samples: 0.7
        };
    }

    return {
        metric_dz: "euclidean",
        normalization_dz: "TIC",
        scaling_dz: "pareto",
        prop_blank_feats_dz: 0.4,
        prop_samples_dz: 0.6,

        "shared-metric": "euclidean",
        "shared-normalization": "TIC",
        "shared-scaling": "pareto",
        "shared-prop_blank_feats": 0.4,
        "shared-prop_samples": 0.6,
    };
}


function fillFormInputs(form, values, formId) {
    Object.entries(values).forEach(([key, value]) => {
        let element = document.getElementById(key);

        if (!element && formId === 'dropzoneForm') {
            const sharedKey = "shared-" + key.replace("_dz", "");
            element = document.getElementById(sharedKey);
            if (element) {
                updateElementValue(element, value);
            }
        } else if (element) {
            updateElementValue(element, value);
        } else {
            console.warn(`Elemento '${key}' não encontrado no formulário '${form.id}'`);
        }
    });
}

function updateElementValue(element, value) {
    if (element.type === 'checkbox') {
        element.checked = value;
        element.value = value ? "true" : "false";
        element.dispatchEvent(new Event('click'));
    } else {
        element.value = value;
        element.dispatchEvent(new Event('change'));
    }
}

async function autoFillCsv(formId) {
    if (formId !== 'dropzoneForm') {
        return;
    }

    try {
        const response = await fetch(FILE_PATH);
        if (!response.ok) throw new Error("Falha ao carregar o CSV");
        if(dropzoneManager.countQueuedFiles() > 1) return;
        const csvText = await response.text();

        const blob = new Blob([csvText], { type: "text/csv" });
        const file = new File([blob], "prefilled.csv", { type: "text/csv" });

        dropzoneManager.addFile(file);
    } catch (error) {
        console.error("Erro ao carregar o CSV:", error);
    }
}


window.prefillForm = prefillForm;



