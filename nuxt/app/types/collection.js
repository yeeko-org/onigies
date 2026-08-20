/**
 * JSDoc contract for `collection_data` — the schema-driven heart of the
 * dashboard. Kept faithful to what the backend emits (`/catalogs/all/`,
 * built in api/ps_schema/registry.py) plus the enrichment applied by
 * `calculateSchemas` in ~/composables/cats.js. No runtime code here:
 * import types via `import('~/types/collection.js').CollectionData`.
 */

/**
 * Field metadata for one model field, computed server-side from Django
 * `model._meta` (`_model_fields` in api/ps_schema/registry.py).
 *
 * @typedef {Object} CollectionField
 * @property {string} name
 * @property {string} real_name Column name: `{name}_id` for relations.
 * @property {boolean} primary_key
 * @property {'simple'|'relation'|'one_to_one'|'one_to_many'|
 *   'many_to_many'} relation_type
 * @property {'unknown'|'text'|'char'|'integer'} field_type
 * @property {boolean} is_string
 * @property {boolean} is_massive
 * @property {boolean} is_editable
 * @property {number} width Suggested column width in px.
 * @property {boolean} null
 * @property {string} [verbose_name]
 * @property {string|number|boolean} [default]
 * @property {number} [max_length] Only for char fields.
 * @property {string} [related_name] Only for relations.
 * @property {string} [related_snake_name] Only for relations.
 * @property {string} [related_model] Only for relations.
 * @property {string} [related_app_label] Only for relations.
 */

/**
 * Presence flags derived server-side from field names
 * (`_derive_field_meta`, HAS_FIELDS).
 *
 * @typedef {Object} CollectionHas
 * @property {boolean} comments
 * @property {boolean} description
 * @property {boolean} help_text
 * @property {boolean} order
 * @property {boolean} color
 * @property {boolean} icon
 */

/**
 * One entry of `available_sorts` (v-select item shape).
 *
 * @typedef {Object} SortOption
 * @property {string} title
 * @property {string} value Ordering param sent to the API.
 */

/**
 * Filter group from the payload (`iter_filter_group_data`), enriched in
 * `calculateSchemas`: `addl_config` is spread at top level and
 * `category_groups` is resolved to the referenced catalog dump.
 *
 * @typedef {Object} FilterGroup
 * @property {string} key_name
 * @property {string} name
 * @property {string} plural_name
 * @property {string} [main_collection] `"app-snake_name"`.
 * @property {Object} addl_config
 * @property {string} [category_group] snake_name of the group catalog.
 * @property {string} [category_type] snake_name of the type catalog.
 * @property {string} [category_subtype] snake_name of the subtype catalog.
 * @property {Object[]} [category_groups] Catalog rows of category_group
 *   (or special_group) — resolved client-side.
 * @property {string} [special_group] From addl_config.
 * @property {string} [prev] Display prefix, from addl_config.
 * @property {string} [short_prev] Short display prefix, from addl_config.
 */

/**
 * Metadata of one status group, from the `status_groups` key of the
 * `/catalogs/all/` payload (`status_groups_data` in api/ies/models.py).
 * Pushed as-is into `collection_filters` for collections with status
 * fields.
 *
 * @typedef {Object} StatusGroup
 * @property {string} key_name `register`, `sending`, `validation`, ...
 * @property {string} collection Field name: `status_{key_name}`.
 * @property {string} name Display name (`de Envío`, ...).
 * @property {string} short_name
 * @property {boolean} hidden
 * @property {number} order
 * @property {string} default_value Initial StatusControl name.
 */

/**
 * One entry of `collection_filters`. Heterogeneous by construction
 * (`calculateSchemas`): a FilterRef merged with its FilterGroup, a
 * custom component filter, a status filter, or the self-filter a
 * category collection pushes for its own level. Discriminate with
 * `is_custom`, `collection` (status) or `forced_level` (self-filter).
 *
 * @typedef {Object} CollectionFilter
 * @property {string} name
 * @property {number} order Sort position in the filter bar.
 * @property {boolean} [hidden]
 * @property {string} [filter_name] FilterRef: key_name of the group.
 * @property {boolean} [can_massive_edit] FilterRef.
 * @property {string} [key_name] From the merged FilterGroup.
 * @property {string} [plural_name]
 * @property {Object} [addl_config]
 * @property {string} [category_group]
 * @property {string} [category_type]
 * @property {string} [category_subtype]
 * @property {Object[]} [category_groups]
 * @property {boolean} [is_custom] ComponentFilter entries.
 * @property {string} [title] ComponentFilter.
 * @property {string} [component] ComponentFilter: Vue component name.
 * @property {string} [field] ComponentFilter: query param it controls.
 * @property {Array} [options] ComponentFilter.
 * @property {Array} [custom_options] ComponentFilter.
 * @property {string} [short_name] Status filters and self-filter.
 * @property {string} [collection] Status filters: `status_{group}`.
 * @property {string} [default_value] Status filters.
 * @property {string} [original_name] Self-filter: name before prefixing.
 * @property {string} [forced_level] Self-filter: level without the
 *   `category_` prefix.
 * @property {boolean} [hide_in_filter]
 */

/**
 * A collection schema as held in `schemas.collections` /
 * `collections_dict` and in `useMainStore.current_collection_data`.
 * Raw payload from api/ps_schema/registry.py (`get_collections_data` +
 * `iter_collection_data`), then enriched by `calculateSchemas`.
 *
 * @typedef {Object} CollectionData
 * @property {string} app_label
 * @property {string} snake_name API route segment and dict key.
 * @property {string} model_name Django model class name.
 * @property {string} name
 * @property {string} plural_name
 * @property {'primary'|'secondary'|'relational'|'category_group'|
 *   'category_type'|'category_subtype'} level
 * @property {Object} cat_params Raw dict; also spread at top level.
 * @property {string[]} sort_fields
 * @property {string[]} extra_massive_edit_fields Non-filter fields
 *   enabled in massive edit.
 * @property {?string} icon
 * @property {?string} color
 * @property {?boolean} open_insertion Allow creating from selects.
 * @property {boolean} optional_category
 * @property {('merge'|'massive_edit'|'massive_delete')[]}
 *   available_actions
 * @property {boolean} xls_export
 * @property {CollectionFilter[]} all_filters Raw declared filters.
 * @property {CollectionField[]} fields
 * @property {string} pk Primary-key field name.
 * @property {?string} name_field `'name'`, `'title'` or null.
 * @property {CollectionHas} has
 * @property {string[]} status_groups Field names related to
 *   StatusControl.
 * @property {number} [order] DB override (Collection table).
 * @property {?string} [help_text] DB override.
 * @property {?string} [description] DB override.
 * @property {CollectionField[]} child_relation_fields Enriched:
 *   one_to_many / many_to_many fields.
 * @property {CollectionField[]} other_fields Enriched: simple fields
 *   not covered by pk, name_field or `has`.
 * @property {boolean} is_category Enriched: level starts with
 *   `category_`.
 * @property {FilterGroup} [filter_group] Enriched: only on category
 *   collections that belong to a filter group.
 * @property {CollectionFilter[]} collection_filters Enriched: resolved
 *   filters, sorted by `order`.
 * @property {SortOption[]} available_sorts Enriched.
 * @property {boolean} [init_display] From cat_params spread: fetch the
 *   list on mount without requiring a filter.
 * @property {boolean} [hide_create] From cat_params spread.
 */

/**
 * Return shape of `calculateSchemas`, held in `useMainStore.schemas`.
 *
 * @typedef {Object} Schemas
 * @property {CollectionData[]} collections
 * @property {Object<string, CollectionData>} collections_dict Keyed by
 *   snake_name.
 * @property {FilterGroup[]} filter_groups
 * @property {{key_name: string, name: string}[]} levels
 * @property {Object<string, FilterGroup>} filters_dict Keyed by
 *   key_name.
 * @property {Object<string, StatusGroup>} status_filters Keyed by the
 *   `status_{group}` field name.
 */

export {}
