# FitExpert Rule Table

Total Rules: **94**

This table documents the executable Python knowledge base used by FitExpert.
The JSON and Markdown versions are generated from `knowledge_base/rules.py` for documentation and viva explanation.

## Age Classification

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-AGE-001 | Classify youth user | 700 | 1.0 | User age is known<br>Age is below 18 | Set age_group = youth | Youth users require conservative exercise programming and supervision-focused recommendations. |
| R-AGE-002 | Classify adult user | 700 | 1.0 | User age is known<br>Age is between 18 and 59 | Set age_group = adult | Adult users can usually follow standard training recommendations unless limited by injuries or medical conditions. |
| R-AGE-003 | Classify senior user | 700 | 1.0 | User age is known<br>Age is 60 or above | Set age_group = senior | Senior users need joint-friendly programming, longer warm-ups, and careful intensity progression. |
| R-AGE-004 | Apply youth safety emphasis | 800 | 0.9 | age_group is youth | Set needs_supervision_focus = True | Youth training should avoid ego lifting and focus on safe movement learning. |
| R-AGE-005 | Apply senior low-impact preference | 800 | 0.85 | age_group is senior | Set needs_low_impact_training = True | Senior users may have higher joint stress risk, so lower-impact training is preferred. |
| R-VOL-009 | Apply conservative volume modifier for senior users | 800 | 0.85 | age_group is senior | Set volume_modifier = conservative_progression | Conservative progression helps reduce recovery and joint-stress problems in senior users. |

## BMI Classification

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-BMI-001 | Classify underweight BMI | 700 | 1.0 | BMI is known<br>BMI is below 18.5 | Set bmi_category = underweight | Underweight users may need conservative volume and strength-building focus. |
| R-BMI-002 | Classify normal BMI | 700 | 1.0 | BMI is known<br>BMI is between 18.5 and 24.9 | Set bmi_category = normal | Normal BMI allows standard program selection based mainly on goal, experience, and equipment. |
| R-BMI-003 | Classify overweight BMI | 700 | 1.0 | BMI is known<br>BMI is between 25 and 29.9 | Set bmi_category = overweight | Overweight BMI may increase joint loading, especially during jumping or running. |
| R-BMI-004 | Classify obese BMI | 700 | 1.0 | BMI is known<br>BMI is 30 or above | Set bmi_category = obese | Obese BMI increases the importance of low-impact conditioning and gradual progression. |
| R-BMI-005 | Detect joint stress risk for overweight user | 700 | 0.75 | bmi_category is overweight | Set joint_stress_risk = moderate | Extra body mass can increase knee and ankle stress during impact-based activities. |
| R-BMI-006 | Detect joint stress risk for obese user | 700 | 0.9 | bmi_category is obese | Set joint_stress_risk = high | Higher BMI can increase impact forces, so safer low-impact training is preferred. |
| R-BMI-007 | Prefer low-impact training for high joint stress | 900 | 0.9 | joint_stress_risk is high | Set needs_low_impact_training = True | Low-impact training reduces unnecessary stress on knees, hips, and ankles. |

## Experience Analysis

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-EXP-001 | Set beginner training volume | 450 | 0.95 | experience_level is beginner | Set training_volume = low | Beginners need lower training volume to learn technique and avoid excessive soreness. |
| R-EXP-002 | Set intermediate training volume | 450 | 0.9 | experience_level is intermediate | Set training_volume = moderate | Intermediate users usually have enough skill and recovery capacity for moderate weekly volume. |
| R-EXP-003 | Set advanced training volume | 450 | 0.85 | experience_level is advanced | Set training_volume = high | Advanced users can use more volume and intensity, but injury rules still override this. |
| R-EXP-004 | Add beginner technique priority | 450 | 0.95 | experience_level is beginner | Set needs_technique_focus = True | Technique focus reduces injury risk and improves long-term progression. |
| R-EXP-005 | Allow advanced progression strategy | 450 | 0.85 | experience_level is advanced<br>No injuries are reported | Set progression_style = advanced_progressive_overload | Advanced users without injuries can progress load, reps, or volume more aggressively. |
| R-VOL-001 | Assign beginner set scheme | 450 | 0.9 | training_volume is low | Set set_scheme = 2_to_3_sets_per_exercise | Beginners should start with fewer sets to learn technique and recover well. |
| R-VOL-002 | Assign intermediate set scheme | 450 | 0.9 | training_volume is moderate | Set set_scheme = 3_to_4_sets_per_exercise | Intermediate users can usually handle moderate set volume while still recovering effectively. |
| R-VOL-003 | Assign advanced set scheme | 450 | 0.85 | training_volume is high | Set set_scheme = 4_to_5_sets_per_main_exercise | Advanced users may benefit from higher volume if safety restrictions do not override it. |

## Schedule Analysis

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-SCH-001 | Select two-day full body split | 400 | 0.95 | available_days is known<br>available_days is 1 or 2 | Set training_split = full_body | With limited weekly availability, full-body sessions cover major movement patterns efficiently. |
| R-SCH-002 | Select three-day full body split | 400 | 0.95 | available_days is 3 | Set training_split = three_day_full_body | A three-day full-body plan balances frequency, recovery, and simplicity. |
| R-SCH-003 | Select four-day upper lower split | 400 | 0.95 | available_days is 4 | Set training_split = upper_lower | Upper/lower split provides good frequency and recovery for four weekly sessions. |
| R-SCH-004 | Select five-day hybrid split | 400 | 0.9 | available_days is 5 | Set training_split = hybrid_strength_conditioning | Five weekly days allow more specialization while still preserving recovery. |
| R-SCH-005 | Select six day push pull legs split | 400 | 0.85 | available_days is known<br>available_days is 6 or more | Set training_split = push_pull_legs | Push/pull/legs works well for frequent training but must be adjusted if safety risks exist. |

## Equipment Analysis

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-EQP-001 | Classify full gym equipment | 600 | 1.0 | equipment is full_gym | Set equipment_level = full | Full gym access allows machines, barbells, dumbbells, and cardio equipment. |
| R-EQP-002 | Classify dumbbell home equipment | 600 | 1.0 | equipment is home_dumbbells | Set equipment_level = limited_weights | Dumbbells support many strength exercises but limit heavy barbell-style progression. |
| R-EQP-003 | Classify bodyweight-only equipment | 600 | 1.0 | equipment is bodyweight_only | Set equipment_level = bodyweight | Bodyweight training requires exercise progressions using leverage, tempo, and volume. |
| R-EQP-004 | Prefer dumbbell variations | 600 | 0.95 | equipment_level is limited_weights | Set exercise_selection_style = dumbbell_based | Home dumbbell users need exercises that match available equipment. |
| R-EQP-005 | Prefer bodyweight progressions | 600 | 0.95 | equipment_level is bodyweight | Set exercise_selection_style = bodyweight_progressions | Bodyweight-only users need movements such as squats, push-ups, bridges, planks, and progressions. |
| R-EQP-006 | Allow machine-supported exercise options | 600 | 0.95 | equipment_level is full | Set exercise_selection_style = full_gym_options | A full gym allows safer machine alternatives, free-weight lifts, and cardio equipment. |
| R-EXS-001 | Select full-gym strength exercise mode | 600 | 0.9 | goal_direction is strength_focused<br>equipment_level is full | Set primary_resistance_mode = compound_lifts_with_machine_support | Full gym access allows compound strength training plus safer machine-supported alternatives. |
| R-EXS-002 | Select dumbbell strength exercise mode | 600 | 0.88 | goal_direction is strength_focused<br>equipment_level is limited_weights | Set primary_resistance_mode = dumbbell_compound_lifts | Dumbbells can support strength work through goblet squats, presses, rows, Romanian deadlifts, and split squats. |
| R-EXS-003 | Select bodyweight strength exercise mode | 600 | 0.85 | goal_direction is strength_focused<br>equipment_level is bodyweight | Set primary_resistance_mode = bodyweight_strength_progressions | Without weights, strength progression can come from harder movement variations, tempo, pauses, and unilateral work. |
| R-EXS-004 | Select full-gym hypertrophy exercise mode | 600 | 0.9 | goal_direction is hypertrophy_focused<br>equipment_level is full | Set primary_resistance_mode = machines_cables_and_free_weights | Hypertrophy training benefits from multiple exercise angles and stable machine or cable options. |
| R-EXS-005 | Select dumbbell hypertrophy exercise mode | 600 | 0.88 | goal_direction is hypertrophy_focused<br>equipment_level is limited_weights | Set primary_resistance_mode = dumbbell_hypertrophy_training | Dumbbells can support muscle gain through presses, rows, lunges, curls, raises, and controlled tempo work. |
| R-EXS-006 | Select bodyweight hypertrophy exercise mode | 600 | 0.82 | goal_direction is hypertrophy_focused<br>equipment_level is bodyweight | Set primary_resistance_mode = bodyweight_volume_training | Bodyweight hypertrophy depends on sufficient volume, controlled tempo, and harder variations. |
| R-EXS-007 | Select bodyweight fat-loss circuit mode | 600 | 0.85 | goal_direction is fat_loss_focused<br>equipment_level is bodyweight | Set primary_resistance_mode = bodyweight_circuit_training | Bodyweight circuits can improve conditioning without needing equipment. |
| R-EXS-008 | Select dumbbell fat-loss circuit mode | 600 | 0.88 | goal_direction is fat_loss_focused<br>equipment_level is limited_weights | Set primary_resistance_mode = dumbbell_circuit_training | Dumbbell circuits combine resistance training and conditioning while fitting home equipment constraints. |
| R-EXS-009 | Select full-gym endurance mode | 600 | 0.9 | goal_direction is endurance_focused<br>equipment_level is full | Set primary_cardio_mode = cardio_machine_supported | Full gym access provides multiple cardio tools, allowing safer selection based on joint tolerance. |

## Medical Safety

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-MED-001 | Detect no medical condition | 1000 | 1.0 | condition_none is True | Set medical_restriction_level = none | No reported medical condition means normal exercise screening can continue. |
| R-MED-002 | Detect asthma condition | 1000 | 0.9 | condition_asthma is True | Set cardio_caution_required = True | Asthma may affect tolerance to intense cardio, so gradual warm-up and controlled intensity are preferred. |
| R-MED-003 | Recommend extended warm-up for asthma | 1000 | 0.9 | cardio_caution_required is True | Set requires_extended_warmup = True | A longer warm-up can reduce sudden intensity spikes for users with asthma. |
| R-MED-004 | Use controlled endurance protocol for asthma | 1000 | 0.85 | condition_asthma is True<br>goal is endurance | Set endurance_protocol = controlled_low_to_moderate_intensity | Endurance training can still be used, but intensity should progress gradually for asthma users. |
| R-INT-006 | Override intensity when medical clearance is required | 1000 | 0.95 | medical_clearance_required is True | Set intensity_profile = clearance_required_before_training | Safety rules override normal training rules when severe injury risk is present. |
| R-CAR-003 | Assign controlled cardio for asthma caution | 1000 | 0.9 | cardio_caution_required is True | Set cardio_frequency = controlled_low_to_moderate_sessions_with_long_warmup | Asthma-related caution should override aggressive cardio prescriptions. |
| R-FIN-004 | Finalize medical-clearance-first plan | 1000 | 0.95 | medical_clearance_required is True | Set final_program_type = medical_clearance_required_before_plan | When severe injury risk exists, safety overrides the normal workout plan generation. |

## Injury Safety

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-INJ-001 | Detect no injury | 900 | 1.0 | injury_none is True | Set injury_restriction_level = none | No reported injury means normal exercise selection can continue. |
| R-INJ-002 | Detect mild knee limitation | 900 | 0.8 | injury_knee is mild | Set knee_risk_level = mild | Mild knee discomfort does not fully block lower-body training but requires careful movement selection. |
| R-INJ-003 | Detect moderate knee limitation | 900 | 0.9 | injury_knee is moderate | Set knee_risk_level = moderate | Moderate knee issues require avoiding jumping, sprinting, and deep knee-dominant exercises. |
| R-INJ-004 | Detect severe knee limitation | 1000 | 0.95 | injury_knee is severe | Set medical_clearance_required = True | Severe knee pain should be evaluated before exercise recommendations are intensified. |
| R-INJ-005 | Prefer knee-safe training | 900 | 0.9 | knee_risk_level is mild or moderate | Set needs_knee_safe_training = True | Knee-safe training reduces high-impact movements and limits painful ranges of motion. |
| R-INJ-006 | Avoid high impact for knee risk | 900 | 0.9 | needs_knee_safe_training is True | Set avoid_high_impact = True | Jumping, sprinting, and aggressive plyometrics can aggravate knee symptoms. |
| R-INJ-007 | Detect lower back limitation | 900 | 0.9 | Lower back injury fact exists<br>Lower back injury severity is mild, moderate, or severe | Set back_risk_level = present | Lower back issues require careful core stability and avoidance of heavy spinal loading. |
| R-INJ-008 | Avoid heavy spinal loading | 900 | 0.9 | back_risk_level is present | Set avoid_heavy_spinal_loading = True | Heavy axial loading may aggravate lower back symptoms. |
| R-INJ-009 | Detect severe lower back issue | 1000 | 0.95 | injury_lower_back is severe | Set medical_clearance_required = True | Severe back pain should be cleared by a professional before exercise intensity is increased. |
| R-INJ-010 | Detect shoulder limitation | 900 | 0.9 | Shoulder injury fact exists<br>Shoulder injury severity is mild, moderate, or severe | Set shoulder_risk_level = present | Shoulder limitations require safer pressing angles and avoidance of painful overhead work. |
| R-INJ-011 | Avoid overhead pressing for shoulder risk | 900 | 0.85 | shoulder_risk_level is present | Set avoid_overhead_pressing = True | Overhead pressing can aggravate shoulder pain if mobility or stability is limited. |
| R-INJ-012 | Detect severe shoulder issue | 1000 | 0.95 | injury_shoulder is severe | Set medical_clearance_required = True | Severe shoulder pain should be professionally assessed before upper-body loading. |
| R-SUB-001 | Select knee-safe lower-body substitutions | 900 | 0.9 | needs_knee_safe_training is True | Set knee_safe_lower_body_options = glute_bridge_box_squat_step_up_partial_range | Knee-safe lower-body choices reduce painful knee flexion and high-impact loading. |
| R-SUB-002 | Select knee-safe cardio substitutions | 900 | 0.9 | needs_knee_safe_training is True | Set knee_safe_cardio_options = walking_cycling_elliptical_if_available | Walking, cycling, and elliptical-style conditioning are usually lower impact than jumping or sprinting. |
| R-SUB-003 | Avoid deep knee flexion when knee risk exists | 900 | 0.85 | needs_knee_safe_training is True | Set avoid_deep_knee_flexion = True | Deep knee flexion may aggravate symptoms in some users with knee limitations. |
| R-SUB-004 | Select lower-back-safe lower-body substitutions | 900 | 0.9 | back_risk_level is present | Set back_safe_lower_body_options = glute_bridge_bird_dog_supported_split_squat | Back-safe substitutions reduce heavy spinal loading and emphasize controlled stability. |
| R-SUB-005 | Select back-safe core training style | 900 | 0.9 | back_risk_level is present | Set core_training_style = anti_extension_and_anti_rotation_core | Anti-extension and anti-rotation core work can build trunk stability without repeated spinal flexion. |
| R-SUB-006 | Avoid loaded hip hinges when back risk exists | 900 | 0.85 | back_risk_level is present | Set avoid_loaded_hinges = True | Heavy loaded hinges may aggravate lower-back symptoms if tolerance is limited. |
| R-SUB-007 | Select shoulder-safe pressing options | 900 | 0.88 | shoulder_risk_level is present | Set shoulder_safe_pressing_options = neutral_grip_press_floor_pushup_landmine_if_available | Neutral-grip and reduced-range pressing options are often more shoulder-friendly than painful overhead pressing. |
| R-SUB-008 | Prioritize pulling balance for shoulder risk | 900 | 0.85 | shoulder_risk_level is present | Set upper_body_balance_priority = rows_rear_delts_scapular_control | Rows, rear-delt work, and scapular control can support shoulder-friendly upper-body programming. |
| R-SUB-009 | Avoid upright rows for shoulder risk | 900 | 0.85 | shoulder_risk_level is present | Set avoid_upright_rows = True | Upright rows can place the shoulder in a position that may be uncomfortable for users with shoulder limitations. |
| R-CAR-004 | Avoid jump-based HIIT when high impact is restricted | 900 | 0.9 | avoid_high_impact is True | Set cardio_avoidance = avoid_jump_based_hiit_and_sprints | When impact is restricted, conditioning should avoid jumps, sprints, and aggressive plyometrics. |

## Goal Analysis

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-GOAL-001 | Set strength goal direction | 500 | 0.95 | goal is strength | Set goal_direction = strength_focused | Strength goals prioritize compound movements, progressive overload, and lower-to-moderate rep ranges. |
| R-GOAL-002 | Set muscle gain goal direction | 500 | 0.95 | goal is muscle_gain | Set goal_direction = hypertrophy_focused | Muscle gain goals prioritize moderate volume, controlled tempo, and progressive resistance. |
| R-GOAL-003 | Set fat loss goal direction | 500 | 0.95 | goal is fat_loss | Set goal_direction = fat_loss_focused | Fat loss goals benefit from resistance training plus conditioning while preserving safety. |
| R-GOAL-004 | Set endurance goal direction | 500 | 0.95 | goal is endurance | Set goal_direction = endurance_focused | Endurance goals prioritize cardiovascular capacity, pacing, and gradual workload progression. |
| R-GOAL-005 | Set flexibility goal direction | 500 | 0.95 | goal is flexibility | Set goal_direction = mobility_focused | Flexibility goals prioritize mobility, stretching, range of motion, and controlled movement quality. |
| R-VOL-004 | Assign strength rep range | 500 | 0.9 | goal_direction is strength_focused | Set rep_range = 3_to_6_reps | Lower repetition ranges support strength development when paired with safe progressive loading. |
| R-VOL-005 | Assign hypertrophy rep range | 500 | 0.9 | goal_direction is hypertrophy_focused | Set rep_range = 8_to_12_reps | Moderate repetition ranges are commonly used for muscle-building programs. |
| R-VOL-006 | Assign fat-loss rep range | 500 | 0.85 | goal_direction is fat_loss_focused | Set rep_range = 10_to_15_reps | Moderate-to-higher reps can support conditioning and movement practice during fat-loss programs. |
| R-VOL-007 | Assign endurance session duration | 500 | 0.9 | goal_direction is endurance_focused | Set cardio_duration = 20_to_40_minutes | Endurance development requires sustained cardiovascular work with gradual progression. |
| R-VOL-008 | Assign flexibility session duration | 500 | 0.9 | goal_direction is mobility_focused | Set mobility_duration = 10_to_20_minutes_daily_or_near_daily | Flexibility improves through consistent practice rather than rare high-intensity sessions. |
| R-EXS-010 | Select flexibility exercise mode | 500 | 0.9 | goal_direction is mobility_focused | Set primary_mobility_mode = mobility_flow_and_static_stretching | A combination of controlled mobility and static stretching supports flexibility goals. |

## Program Direction

| Rule ID | Rule Name | Salience | CF | IF Conditions | THEN Actions | Explanation |
|---|---|---:|---:|---|---|---|
| R-GOAL-006 | Prefer low-impact fat loss when overweight | 300 | 0.85 | goal_direction is fat_loss_focused<br>bmi_category is overweight or obese | Set conditioning_style = low_impact_fat_loss | Low-impact conditioning supports fat loss while reducing unnecessary joint stress. |
| R-GOAL-007 | Prefer technique-first strength for beginners | 300 | 0.9 | goal_direction is strength_focused<br>experience_level is beginner | Set program_emphasis = technique_first_strength | Beginner strength training should build skill before heavier loading. |
| R-GOAL-008 | Prefer mobility base for flexibility goal | 300 | 0.9 | goal_direction is mobility_focused | Set program_emphasis = mobility_and_control | Flexibility improves best when stretching is combined with controlled range-of-motion practice. |
| R-INT-001 | Set strength intensity profile | 300 | 0.9 | goal_direction is strength_focused | Set intensity_profile = strength_low_reps_progressive_load | Strength programs usually emphasize heavier resistance, lower repetitions, and gradual load progression. |
| R-INT-002 | Set hypertrophy intensity profile | 300 | 0.9 | goal_direction is hypertrophy_focused | Set intensity_profile = moderate_reps_muscle_tension | Hypertrophy training benefits from moderate repetitions, sufficient volume, and controlled movement tempo. |
| R-INT-003 | Set fat-loss intensity profile | 300 | 0.9 | goal_direction is fat_loss_focused | Set intensity_profile = resistance_plus_conditioning | Fat-loss programs should combine strength work with safe conditioning to improve energy expenditure while preserving muscle. |
| R-INT-004 | Set endurance intensity profile | 300 | 0.9 | goal_direction is endurance_focused | Set intensity_profile = aerobic_base_progression | Endurance training should gradually build aerobic capacity before intense intervals are emphasized. |
| R-INT-005 | Set flexibility intensity profile | 300 | 0.9 | goal_direction is mobility_focused | Set intensity_profile = controlled_mobility_and_stretching | Flexibility-focused users should prioritize controlled range of motion, breathing, and gradual stretch tolerance. |
| R-CAR-001 | Assign low-impact fat-loss cardio frequency | 300 | 0.85 | conditioning_style is low_impact_fat_loss | Set cardio_frequency = 3_to_4_low_impact_sessions_per_week | Low-impact cardio several times per week supports fat loss while limiting joint stress. |
| R-CAR-002 | Assign endurance cardio frequency | 300 | 0.88 | goal_direction is endurance_focused<br>condition_none is True | Set cardio_frequency = 3_progressive_endurance_sessions_per_week | Endurance users without medical caution can progress cardio frequency gradually. |
| R-FIN-001 | Finalize beginner low-impact fat-loss plan | 100 | 0.9 | goal_direction is fat_loss_focused<br>experience_level is beginner<br>training_split is upper_lower<br>conditioning_style is low_impact_fat_loss | Set final_program_type = beginner_4_day_low_impact_fat_loss | The final plan combines beginner status, fat-loss goal, four-day availability, and joint-friendly conditioning. |
| R-FIN-002 | Finalize beginner strength foundation plan | 100 | 0.88 | goal_direction is strength_focused<br>experience_level is beginner<br>needs_technique_focus is True | Set final_program_type = beginner_strength_foundation | Beginner strength users should follow a foundation plan focused on technique and gradual loading. |
| R-FIN-003 | Finalize dumbbell hypertrophy split | 100 | 0.86 | goal_direction is hypertrophy_focused<br>equipment_level is limited_weights<br>training_split is upper_lower | Set final_program_type = dumbbell_upper_lower_hypertrophy | A four-day upper/lower split works well for dumbbell-based muscle gain training. |
