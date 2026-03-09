<script setup>

import { useMainStore } from '~/store/index.js'
import { useIesStore } from '~/store/ies.js'
const mainStore = useMainStore()
const iesStore = useIesStore()
import {storeToRefs} from "pinia";

const { ies_data } = storeToRefs(iesStore);
const dialog_edit = ref(false)
const dialogForm = ref(null)
const edit_data = ref({
  id: null,
  name: '',
  acronym: '',
  is_public: false
})
const loading = ref(false)

function startEdit(){
  edit_data.value = {
    id: ies_data.value.id,
    name: ies_data.value.name,
    acronym: ies_data.value.acronym,
    is_public: ies_data.value.is_public,
  }
  dialog_edit.value = true
}

function indirectClick(){
  document.getElementById("logo").click();
}

async function changeLogo(e){
  loading.value = true
  // console.log(e)
  let file = e.target.files[0] || e.dataTransfer.files[0];

  let formData = new FormData();
  formData.append("logo", file, file.name);
  const request = {
    data: formData,
    institution_id: ies_data.value.id,
    snack_text: "Tu logo ha sido actualizado"
  }

  const res = await iesStore.updateLogo(request)
  if (res.errors){
    console.errors(res.errors)
  }
  loading.value = false

}

async function saveInstitutionData(){
  loading.value = true
  const res = await mainStore.saveSimple(['institution', edit_data.value])
  if (res.errors) {

    console.error(res.errors)
  }
  else {
    iesStore.ies_data = {
      ...iesStore.ies_data,
      ...res
    }
    dialog_edit.value = false
  }
  loading.value = false
}

</script>

<template>
  <v-card
    v-if="ies_data"
    variant="outlined"
    class="w-100 my-4"
  >
    <div class="d-flex flex-no-wrap ">
      <input
        type="file"
        accept="image/*"
        id="logo"
        style="display:none"
        @change="changeLogo"
      >
      <v-avatar
        class="ma-3"
        rounded="0"
        size="200"
      >
        <v-img
          v-if="ies_data.logo"
          :src="ies_data.logo"
        ></v-img>
        <v-empty-state
          v-else
          headline="Sin logo"
          icon="owl"
          bg-color="#fdefff"
          text="Agrega el logo de tu institución"
        >
          <template v-if="false" v-slot:media>
            <v-sheet class="py-4 mb-4" color="#fdefff">
              <v-icon
                size="48"
                color="pink"
              >
                owl
              </v-icon>
            </v-sheet>
          </template>
        </v-empty-state>
      </v-avatar>

      <div>
        <v-card-title class="text-h4 pb-1 font-weight-bold">
          {{ies_data.acronym}}
        </v-card-title>
        <v-card-title class="text-h5 text-black pt-0 pb-4">
          {{ies_data.name}}
        </v-card-title>
        <v-card-text>
          <v-chip
            size="small"
            color="primary"
          >
            Institución {{ ies_data.is_public ? 'pública' : 'privada' }}
          </v-chip>
        </v-card-text>
        <v-card-actions>
          <v-btn
            class="ms-2"
            size="small"
            text="Editar datos"
            :variant="ies_data.logo ? 'outlined' : 'elevated'"
            color="accent"
            @click="startEdit"
          ></v-btn>
        </v-card-actions>
      </div>

    </div>
    <v-dialog
      v-model="dialog_edit"
      width="800"
    >
      <v-card v-if="edit_data" width="800">
        <v-form
          ref="dialogForm"
        >
          <div class="ga-2 d-flex">
            <div class="d-flex flex-column align-center">
              <v-avatar
                class="mx-3 my-6"
                rounded="0"
                size="200"
              >
                <v-img
                  v-if="ies_data.logo"
                  :src="ies_data.logo"
                ></v-img>
                <v-empty-state
                  v-else
                  headline="Sin logo"
                  icon="owl"
                  bg-color="#fdefff"

                >
                  <template #actions>
                    <v-btn
                      variant="elevated"
                      color="accent"
                      size="small"
                      @click="indirectClick"
                    >
                      Agregar logo
                    </v-btn>
                  </template>
                </v-empty-state>
              </v-avatar>
              <v-btn
                variant="outlined"
                color="accent"
                size="small"
                @click="indirectClick"
              >
                Cambiar logo
              </v-btn>

            </div>
            <v-card-text>
              <v-card-title class="px-0 pt-0 pb-5 d-flex align-center">
                Editar datos de la Institución
                <v-spacer/>
                <v-btn
                  variant="text"
                  color="grey"
                  size="small"
                  class="ms-4"
                  icon
                  @click="dialog_edit = false"
                >
                  <v-icon>
                    close
                  </v-icon>
                </v-btn>
              </v-card-title>
              <v-text-field
                v-model="edit_data.name"
                label="Nombre de la Universidad"
                variant="outlined"
              />
              <v-text-field
                v-model="edit_data.acronym"
                label="Siglas"
                variant="outlined"

              />
              <v-switch
                v-model="edit_data.is_public"
                label="¿Es una institución pública?"
                variant="outlined"
                hide-details
                color="accent"
              />
            </v-card-text>
          </div>
        </v-form>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            variant="text"
            @click="dialog_edit = false"
            color="grey"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="accent"
            variant="elevated"
            @click="saveInstitutionData"
          >
            Guardar cambios
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>