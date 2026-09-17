/* =========================================================
   FIELDGUARD
   Live Three-Zone Monitoring Simulation
   ========================================================= */


/* ---------------------------------------------------------
   Determine zone condition from temperature
   --------------------------------------------------------- */

function getZoneStatus(temperature) {

    if (temperature >= 30) {
        return "CRITICAL";
    }

    if (temperature >= 25) {
        return "WARNING";
    }

    return "NORMAL";
}


/* ---------------------------------------------------------
   Update an individual sensing zone
   --------------------------------------------------------- */

function updateZone(zoneNumber) {

    const slider =
        document.getElementById(`slider${zoneNumber}`);

    const temperatureDisplay =
        document.getElementById(`temp${zoneNumber}`);

    const statusDisplay =
        document.getElementById(`status${zoneNumber}`);


    const temperature =
        Number(slider.value);

    const status =
        getZoneStatus(temperature);


    /* Update displayed temperature */

    temperatureDisplay.textContent =
        temperature;


    /* Update zone status */

    statusDisplay.textContent =
        status;


    /* Update badge appearance */

    statusDisplay.className =
        `status ${status.toLowerCase()}`;


    /* Update central FieldGuard receiver */

    updateReceiver();
}


/* ---------------------------------------------------------
   Update central receiver
   --------------------------------------------------------- */

function updateReceiver() {

    const criticalZones = [];
    const warningZones = [];


    /* Check all three sensing zones */

    for (let zone = 1; zone <= 3; zone++) {

        const status =
            document
                .getElementById(`status${zone}`)
                .textContent;


        if (status === "CRITICAL") {

            criticalZones.push(zone);

        }

        else if (status === "WARNING") {

            warningZones.push(zone);

        }
    }


    const receiverStatus =
        document.getElementById("receiverStatus");

    const receiverMessage =
        document.getElementById("receiverMessage");


    /* -----------------------------------------------------
       Priority 1 — CRITICAL
       ----------------------------------------------------- */

    if (criticalZones.length > 0) {

        receiverStatus.textContent =
            "CRITICAL CONDITION";

        receiverMessage.textContent =
            createZoneMessage(
                "Attention required in",
                criticalZones
            );

        return;
    }


    /* -----------------------------------------------------
       Priority 2 — WARNING
       ----------------------------------------------------- */

    if (warningZones.length > 0) {

        receiverStatus.textContent =
            "WARNING CONDITION";

        receiverMessage.textContent =
            createZoneMessage(
                "Monitor",
                warningZones
            );

        return;
    }


    /* -----------------------------------------------------
       Priority 3 — NORMAL
       ----------------------------------------------------- */

    receiverStatus.textContent =
        "SYSTEM NORMAL";

    receiverMessage.textContent =
        "All monitored zones are within normal limits.";
}


/* ---------------------------------------------------------
   Create readable zone messages

   Examples:

   Attention required in Zone 3.

   Attention required in Zone 1 and Zone 3.

   Attention required in Zone 1, Zone 2 and Zone 3.
   --------------------------------------------------------- */

function createZoneMessage(prefix, zones) {

    if (zones.length === 1) {

        return `${prefix} Zone ${zones[0]}.`;

    }


    if (zones.length === 2) {

        return (
            `${prefix} Zone ${zones[0]} and Zone ${zones[1]}.`
        );

    }


    const lastZone =
        zones[zones.length - 1];


    const previousZones =
        zones
            .slice(0, -1)
            .map(zone => `Zone ${zone}`)
            .join(", ");


    return (
        `${prefix} ${previousZones} and Zone ${lastZone}.`
    );
}


/* ---------------------------------------------------------
   Initialise FieldGuard simulation
   --------------------------------------------------------- */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        updateZone(1);
        updateZone(2);
        updateZone(3);

    }
);
