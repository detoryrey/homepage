document.addEventListener('DOMContentLoaded', () => {
    function initCarouselBlock({
                                   blockId,
                                   carouselId,
                                   titleSelector,
                                   descSelector,
                                   iconsSelector,
                                   data,
                                   activeClass = 'act'
                               }) {
        const block = document.getElementById(blockId);
        if (!block) {
            console.warn('Block not found:', blockId);
            return;
        }

        const icons = block.querySelectorAll(iconsSelector);
        const carouselEl = block.querySelector('#' + carouselId);
        const titleEl = block.querySelector(titleSelector) || document.querySelector(titleSelector);
        const descEl = block.querySelector(descSelector) || document.querySelector(descSelector);

        if (!carouselEl || !titleEl || !descEl) {
            console.warn('Missing elements in block:', blockId);
            return;
        }
        const carousel = bootstrap.Carousel.getOrCreateInstance(carouselEl, {interval: 8000});


        icons.forEach((img, i) => {
            img.addEventListener('click', () => {
                carousel.to(i);
                updateText(i);
                highlight(i);
            });
        });

        carouselEl.addEventListener('slid.bs.carousel', (e) => {
            const i = e.to;
            updateText(i);
            highlight(i);
        });

        function updateText(i) {
            if (!data[i]) return;
            titleEl.textContent = data[i].name;
            descEl.innerHTML = data[i].desc;
        }

        function highlight(i) {
            icons.forEach(img => img.classList.remove(activeClass));
            if (icons[i]) icons[i].classList.add(activeClass);
        }

        const items = carouselEl.querySelectorAll('.carousel-item');
        const startIdx = [...items].findIndex(el => el.classList.contains('act'));
        const initIdx = startIdx >= 0 ? startIdx : 0;
        updateText(initIdx);
        highlight(initIdx);

    }

    const dataGame = [
        {
            name: "Infinity Nikky",
            desc: "Join Nikki and Momo in a vast fantasy world, exploring freely and savoring varied playstyles. The power resting in gorgeous outfits will find you a path forward and offer infinite fun along the journey!"
        },
        {
            name: "Genshin Impact",
            desc: "Genshin Impact is an open-world adventure game. In the world of Teyvat &mdash; where all kinds of elemental powers constantly surge &mdash; epic adventures await, fearless travelers!"
        },
        {
            name: "Wuthering Waves",
            desc: "This is a story-rich open-world game with a high degree of freedom. You wake from your slumber as a Rover, greeted by an expansive new world filled with novel sights and newfangled tech."
        },
        {
            name: "Assassin's Creed II",
            desc: "An epic tale of family, vengeance, and conspiracy set in Renaissance Italy. Ezio faces Florence&rsquo;s powerful families and, through the canals of Venice, rises to become a master assassin."
        }
    ];


    const dataBook = [
        {
            name: "Throne of glass",
            desc: "In a land without magic, assassin Celaena Sardothien is brought to the king&rsquo;s castle&ndash;not to kill, but to fight for her freedom. To earn it, she must defeat twenty-three ruthless opponents in a deadly competition and serve as the King&rsquo;s Champion."
        },
        {
            name: "Mistborn",
            desc: "For a thousand years, ash has fallen and the Skaa have lived in fear, enslaved under the immortal Lord Ruler. Hope was lost&ndash;until Kelsier, a scarred half-Skaa thief who discovered the powers of a Mistborn, dared to dream of rebellion."
        },
        {
            name: "Harry Potter",
            desc: "For ten years, Harry Potter lived in misery with his cruel aunt and uncle. Hope seemed lost&ndash;until on his eleventh birthday, he discovered he was a wizard and destined to attend Hogwarts School of Witchcraft and Wizardry."
        },
        {
            name: "The Poppy War",
            desc: "Rin, a war orphan from Rooster Province, shocked everyone by acing the Keju and earning a place at Sinegard. Targeted for her color and poverty, she discovers a deadly shamanic power that could save her people &mdash; or destroy her."
        },
        {
            name: "A Song of Ice and Fire",
            desc: "Long ago, the seasons fell out of balance, and winter returns. In the north, dark forces gather, while in the south, the king&rsquo;s power falters. Eddard Stark is called to serve as Hand, risking his family and the kingdom."
        },
        {
            name: "The Way of Kings",
            desc: "On storm-ravaged Roshar, ancient Shardblades still spark war. On the Shattered Plains, once a healer, is now a slave Kaladin fights to protect his men, Dalinar is haunted by visions, and Shallan pursues dangerous secrets."
        }
    ]
    initCarouselBlock({
        blockId: 'blockTWO',
        carouselId: 'carouselTWO',
        titleSelector: '#NamesGames',
        descSelector: '#descriptionGames',
        iconsSelector: '.additional-icon',
        data: dataGame,
        activeClass: 'act'
    });

    initCarouselBlock({
        blockId: 'blockTHREE',
        carouselId: 'carouselTHREE',
        titleSelector: '#NamesBooks',
        descSelector: '#descriptionBooks',
        iconsSelector: '.additional-icon',
        data: dataBook,
        activeClass: 'act'
    });

    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
      if (window.scrollY > 0) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
    document.addEventListener('show.bs.dropdown', function (e) {
      // закриваємо всі відкриті dropdown-и, крім того, який відкривається зараз
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        if (menu !== e.target.querySelector('.dropdown-menu')) {
          bootstrap.Dropdown.getInstance(menu.closest('.dropdown-toggle') || menu.previousElementSibling)?.hide();
        }
      });
    });
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
      // отримуємо положення меню та ширину вікна
      const rect = menu.getBoundingClientRect();
      const overflowRight = rect.right - window.innerWidth;

      if (overflowRight > 0) {
        // зсуваємо меню вліво на потрібну величину
        menu.style.left = `-${overflowRight}px`;
      } else {
        menu.style.left = '0';
      }
    });
});


