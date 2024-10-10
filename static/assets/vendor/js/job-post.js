// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById("jobPosition").addEventListener("change", function () {
//         const jobPosition = this.value;

//         if (jobPosition) {
//             fetch(`/get_personality_traits/?job_position=${jobPosition}`)
//                 .then((response) => response.json())
//                 .then((data) => {
//                     console.log("Received data:", data);

//                     // Clear existing options in the dropdown
//                     const personalityTraitsDropdown = document.getElementById("personalityTraitsDropdown");
//                     personalityTraitsDropdown.innerHTML = "";

//                     // Combine data from personality traits, cognitive skills, and emotional intelligence
//                     const combinedTraits = [...new Set([
//                         ...data.personality_traits,
//                         ...data.cognitive_skills,
//                         ...data.emotional_intelligence
//                     ])];

//                     // Populate dropdown with combined data
//                     combinedTraits.forEach((trait) => {
//                         const option = document.createElement("option");
//                         option.value = trait;
//                         option.textContent = trait;
//                         personalityTraitsDropdown.appendChild(option);
//                     });

//                     // Set recommended weightage values
//                     document.getElementById("recommendedCognitiveWeightage").textContent = data.cognitive_weightage || "N/A";
//                     document.getElementById("recommendedTechnicalWeightage").textContent = data.technical_weightage || "N/A";
//                 })
//                 .catch((error) => console.error("Error fetching data:", error));
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("jobPosition").addEventListener("change", function () {
        const jobPosition = this.value;
        
        console.log("Selected job position:", jobPosition);  // Add this to verify the selected value

        if (jobPosition) {
            fetch(`/get_personality_traits/?job_position=${jobPosition}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log("Received data:", data);  // Confirm the data from the backend

                    // Clear existing options in the dropdown
                    const personalityTraitsDropdown = document.getElementById("personalityTraitsDropdown");
                    personalityTraitsDropdown.innerHTML = "";

                    // Combine data from personality traits, cognitive skills, and emotional intelligence
                    const combinedTraits = [...new Set([
                        ...data.personality_traits,
                        ...data.cognitive_skills,
                        ...data.emotional_intelligence
                    ])];

                    // Populate dropdown with combined data
                    combinedTraits.forEach((trait) => {
                        const option = document.createElement("option");
                        option.value = trait;
                        option.textContent = trait;
                        personalityTraitsDropdown.appendChild(option);
                    });

                    // Set recommended weightage values
                    document.getElementById("recommendedCognitiveWeightage").textContent = data.cognitive_weightage || "N/A";
                    document.getElementById("recommendedTechnicalWeightage").textContent = data.technical_weightage || "N/A";
                })
                .catch((error) => console.error("Error fetching data:", error));
        }
    });
});
