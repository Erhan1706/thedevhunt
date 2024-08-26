document.addEventListener("DOMContentLoaded", function () {
  const triggers = document.querySelectorAll(".popover-trigger");

  triggers.forEach((trigger) => {
    const popover = document.querySelector(".popover");

    // Make the text in the popover be coming soon
    //popover.textContent = 'Coming soon';
    //document.body.appendChild(popover);

    trigger.addEventListener("mouseenter", function (e) {
      const rect = trigger.getBoundingClientRect();
      popover.style.left = `${rect.left}px`;
      popover.style.top = `${rect.bottom + window.scrollY}px`;
      popover.style.display = "block";
    });

    trigger.addEventListener("mouseleave", function () {
      popover.style.display = "none";
    });
  });
});
