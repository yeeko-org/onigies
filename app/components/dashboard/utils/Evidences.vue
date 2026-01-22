<script setup>
import {useMainStore} from "~/stores/index.js";
const mainStore = useMainStore()

const props = defineProps({
  full_main: {
    type: Object,
    required: true,
  },
  main_collection_name: String,
})

const saving = ref(false)
const main_file = ref(null)
const dialog_file_trash = ref(false)

const file_id = `evidence-${props.full_main.id}`

function indirectAdd(){
  document.getElementById(file_id).click()
}

function uploadFile(e){
  let files = e.target.files || e.dataTransfer.files;
  // console.log("files", files)
  const first_file = files[0]
  main_file.value = {file: first_file, url: URL.createObjectURL(first_file)}
  sendFile()
}

function sendFile(){
  let formData = new FormData();
  formData.append("file", main_file.value.file, main_file.value.file.name);
  const elem_id = props.full_main.id
  const params = [elem_id, formData, props.main_collection_name]
  mainStore.saveFile(params).then(res=>{
    // ready_files.value += 1
    saving.value = false
    props.full_main.evidences.push(res)
    main_file.value = null
  })
}

function trashFile(file){
  console.log("trashFile", file)
  main_file.value = file
  dialog_file_trash.value = true
}

function deleteFile(){
  saving.value = true
  // const elem_id = props.full_main.id
  const params = ['evidence', main_file.value.id]
  mainStore.deleteSimple(params).then(res=>{
    saving.value = false
    props.full_main.evidences = props.full_main.evidences.filter(
      e=>e.id !== main_file.value.id)
    main_file.value = null
    dialog_file_trash.value = false
  })
}

// const evidences = computed(()=>{
//   return props.full_main.evidences.map(ev)
// })



</script>

<template>
  <v-chip
    v-for="item in full_main.evidences"
    :key="item.id"
    :href="item.url ? item.url : item.file_url"
    target="_blank"
    class="ml-6 px-6 my-1"
    color="accent lighten-1"
    text-color="red"
    prepend-icon="picture_as_pdf"
  >
    <span class="white--text" v-if="item.url">
      {{item.name}}
    </span>
    <span class="white--text" v-else>
      {{item.file.name}}
    </span>
    <template v-slot:append>
      <v-icon
        small
        class="white--text ml-2"
        @click.stop="trashFile(item.file)"
        color="error"
      >
        delete
      </v-icon>
    </template>
  </v-chip>
  <input
    type="file"
    :id="file_id"
    style="display:none"
    @change="uploadFile($event)"
  >

<!--    <v-file-input-->
<!--      ref="new_file"-->
<!--      label="Subir archivo"-->
<!--      name="logo"-->
<!--      variant="solo"-->
<!--      rounded="lg"-->
<!--      hide-details-->
<!--      density="compact"-->
<!--      class="mr-2"-->
<!--      bg-color="success"-->
<!--      :loading="saving"-->
<!--      @change="uploadFile($event)"-->
<!--      style="max-width: 200px;"-->
<!--    ></v-file-input>-->
  <v-btn
    @click="indirectAdd"
    variant="outlined"
    color="accent"
    :loading="saving"
    class="ml-2 mt-1"
    append-icon="attach_file"
  >
    Agregar archivo
  </v-btn>
  <v-dialog
    v-model="dialog_file_trash"
    max-width="350"
  >
    <v-card>
      <v-card-title class="headline">
        ¿De verdad quieres eliminar el archivo?
      </v-card-title>
      <v-card-text>
        Una vez eliminado no lo podrás recuperar
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          variant="text"
          @click="dialog_file_trash = false"
        >
          No eliminar
        </v-btn>
        <v-btn
          color="primary"
          variant="text"
          @click="deleteFile"
        >
          Sí eliminar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<style scoped>

</style>