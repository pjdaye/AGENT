start: observation_list SPACE component_action_list 
        SPACE observation_list  -> test_flow

observation_list: observation SPACE observation_list
                 -> observation_list_sublist
                | observation -> observation_list_single

observation: "OBSERVE" SPACE qualifier_list? SPACE? 
                component -> observe
             | "NOTOBSERVE" SPACE qualifier_list? SPACE? 
                component -> not_observe
             | "OBSERVE" SPACE capture SPACE "IN" SPACE 
                "COLLECTION" -> observe_in_collection
             | "NOTOBSERVE" SPACE capture SPACE "IN" SPACE 
                "COLLECTION" -> not_observe_in_collection
             | "OBSERVE" SPACE qualifier_list? SPACE? component
                SPACE capture -> observe_capture
             | "OR(" SPACE conditional_observations SPACE ")" 
                -> conditional_observation_list

conditional_observations: observation SPACE "," SPACE 
                conditional_observations 
                  -> conditional_list_sublist
             | observation -> conditional_list_single

qualifier_list: qualifier SPACE qualifier_list 
                  -> qualifier_list_sublist
                | qualifier -> qualifier_list_single

qualifier: "REQUIRED" -> required
         | "DISABLED" -> disabled
         | "SCREEN" -> screen
         | learned_qualifier

component_action_list: component_action SPACE 
                        component_action_list_single
                        -> component_action_list_sublist
                     | component_action 
                        -> component_action_list_single

component_action: "TRY" SPACE equivalence_class SPACE 
                        component -> try_
                | "TRY" SPACE equivalence_class SPACE 
                        component SPACE capture -> try_capture
                | "TRY" SPACE (capture|not_capture) SPACE 
                        component -> try_captured
                | "CLICK" SPACE component -> click
                | "ENTER" SPACE component -> enter
                | "NAVIGATE" SPACE component -> navigate
                | "FOCUS" SPACE capture SPACE "IN" SPACE 
                        "COLLECTION" -> focus_in_collection

component: element_class SPACE TOKEN -> component_1
         | element_class -> component_2
         | TOKEN -> component_3

equivalence_class: "VALID" -> valid
                 | "INVALID" -> invalid
                 | "BLANK" -> blank
                 | "WHITESPACE" -> whitespace
                 | "INVALID_LONG" -> invalid_long
                 | "INVALID_SPECIAL_CHARACTERS" 
                    -> invalid_special_characters
                 | "INVALID" -> invalid
                 | "INVALID_XSR" -> invalid_xsr
                 | learned_eq_class

element_class: "TEXTBOX" -> textbox
             | "DROPDOWN" -> dropdown
             | "ERRORMESSAGE" -> error_message
             | "COMMIT" -> commit
             | "CANCEL" -> cancel
             | learned_el_class

capture: "$" TOKEN -> capture

not_capture: "!" TOKEN -> not_capture

learned_qualifier: "LEARNED_QUAL_" TOKEN

learned_eq_class: "LEARNED_EQCLASS_" TOKEN

learned_el_class: "LEARNED_ELCLASS_" TOKEN

TOKEN: /_?[A-Z][_A-Z0-9]*/

%import common.WS -> SPACE

%import common.ESCAPED_STRING -> _STRING