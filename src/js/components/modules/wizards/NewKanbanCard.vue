<template>
    <div class="modal fade" 
         id="addKanbanCardModal" 
         tabindex="-1" 
         aria-labelledby="addKanbanCardModalLabel" 
         aria-hidden="true"
         v-bind:data-kanban-level="levelResults[0]['pk']"
         v-bind:data-kanban-column="columnResults[0]['pk']"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><Icon v-bind:icon="icons.cardChecklist"></Icon> Add Kanban Card Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="addKanbanCardCloseButton"
                    ></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Please note</strong>
                            <p class="text-instructions">
                                The card names can not be the same as something that already exists on the board.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label>Kanban Card Text</label>
                            <input v-model="kanbanCardTextModel"
                                   v-on:keydown.enter="addKanbanCard"
                                   class="form-control"
                            >
                        </div>
                    </div>
                    <!-- CARD DESCRIPTION -->
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Card Description</strong>
                            <p class="text-instructions">
                                Fill out a detailed description for the card, then click on the "Update Card" button
                                to update the card.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <editor
                               :init="{
                                 file_picker_types: 'image',
                                 height: 300,
                                 images_upload_handler: uploadImage,
                                 menubar: false,
                                 paste_data_images: true,
                                 plugins: ['lists','paste','table'],
                                  toolbar: [
                                     'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                                     'bold italic strikethrough underline backcolor | table | ' +
                                     'bullist numlist outdent indent | removeformat'
                                  ]}"
                               v-bind:content_css="false"
                               v-bind:skin="false"
                               v-model="kanbanCardDescriptionModel"
                            />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-on:click="addKanbanCard"
                            v-bind:disabled="disableAddButton"
                    >
                        Add Card
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { Icon } from '@iconify/vue';
    import Editor from '@tinymce/tinymce-vue'

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";
    import uploadMixin from "../../../mixins/uploadMixin";

    export default {
        name: "NewKanbanCard",
        components: {
            'editor': Editor,
            Icon,
        },
        props: {
            columnResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            kanbanCardResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            levelResults:  {
                type: Array,
                default: () => {
                    return [];
                },
            },
            kanbanBoardResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        mixins: [
            iconMixin,
            uploadMixin,
        ],
        data() {
            return {
                disableAddButton: true,
                kanbanCardDescriptionModel: '',
                kanbanCardTextModel: '',
            }
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
            })
        },
        methods: {
            addKanbanCard: function() {
                //Get the modal to extract data from
                var self_modal = document.getElementById('addKanbanCardModal');

                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('kanban_card_text',this.kanbanCardTextModel);
                data_to_send.set('kanban_card_description',this.kanbanCardDescriptionModel);
                data_to_send.set('kanban_level',self_modal['dataset']['kanbanLevel']);
                data_to_send.set('kanban_column',self_modal['dataset']['kanbanColumn']);

                //Send the data
                axios.post(
                    `${this.rootUrl}kanban_information/${this.kanbanBoardResults[0]['pk']}/new_card/`,
                    data_to_send,
                ).then(response => {
                    //Emit the data upstream
                    this.$emit('new_card',response['data']);

                    //Blank the model
                    this.kanbanCardTextModel = '';
                    this.kanbanCardDescriptionModel = '';

                    //Close the modal
                    document.getElementById('addKanbanCardCloseButton').click();
                }).catch(error => {
                    
                });
            },
        },
        watch: {
            kanbanCardTextModel: function() {
                // If the model is blank OR the text already exists - turn disableAddButton to true
                this.disableAddButton = false; //People can click the "Add" button

                if (this.kanbanCardTextModel.length == 0) {
                    this.disableAddButton = true;
                }

                //Check to make sure it does not exist
                var filtered_results = this.kanbanCardResults.filter(row => {
                    return row['fields']['kanban_card_text'] == this.kanbanCardTextModel;
                });

                if (filtered_results.length > 0) {
                    this.disableAddButton = true;
                }

                //If there are no rows or levels - we don't want the user to submit a card
                if (this.columnResults.length == 0 || this.levelResults.length == 0) {
                    this.disableAddButton = true;
                }
            },
        }
    }
</script>

<style scoped>

</style>
