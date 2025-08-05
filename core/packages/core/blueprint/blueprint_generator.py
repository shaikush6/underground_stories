#!/usr/bin/env python3
"""
Underground Stories Blueprint Generator
======================================

Generates detailed story blueprints from simple concepts using the expanded format
that creates rich, detailed foundation for excellent short stories.
"""

import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

@dataclass
class OriginalStoryBlueprint:
    """Structure for original fairy tale blueprint"""
    title: str
    genre: str
    logline: str
    character: str
    conflict: str
    setting: str
    theme: str
    exposition: str
    inciting: str
    rising: str
    climax: str
    falling: str
    resolution: str

@dataclass
class DetailedStoryComponent:
    """Detailed expansion of a story component"""
    component: str
    expanded_description: str

@dataclass
class NewStoryBlueprint:
    """Structure for new Underground Stories blueprint"""
    title: str
    genre: str
    logline: str
    character: DetailedStoryComponent
    conflict: DetailedStoryComponent
    setting: DetailedStoryComponent
    theme: DetailedStoryComponent
    exposition: DetailedStoryComponent
    inciting_incident: DetailedStoryComponent
    rising_action: DetailedStoryComponent
    climax: DetailedStoryComponent
    falling_action: DetailedStoryComponent
    resolution: DetailedStoryComponent

@dataclass
class CompleteBlueprint:
    """Complete blueprint with original and new versions"""
    story_id: int
    original: OriginalStoryBlueprint
    new: NewStoryBlueprint
    generated_at: str
    blueprint_prompt_version: str

class BlueprintGenerator:
    """
    Advanced blueprint generator using the detailed expansion methodology.
    Creates rich, detailed blueprints optimal for story generation.
    """
    
    def __init__(self):
        self.blueprints_dir = Path("content/blueprints")
        self.blueprints_dir.mkdir(parents=True, exist_ok=True)
        
        # Story mapping for original fairy tales
        self.fairy_tale_base = {
            "huff_heal": {
                "original_title": "Little Red Riding Hood & Big Bad Wolf",
                "genre": "Folk Horror / Cautionary Tale",
                "base_logline": "A girl encounters a dangerous wolf while visiting her grandmother",
                "characters": "Red Riding Hood: innocent child, Wolf: predatory threat, Grandmother: vulnerable elder",
                "conflict": "Child's naivety vs. predator's cunning",
                "setting": "Dark forest path to grandmother's cottage",
                "themes": "Stranger danger, loss of innocence, predator-prey dynamics"
            },
            "high_crimes": {
                "original_title": "Jack and the Beanstalk", 
                "genre": "Heroic Folk-Tale",
                "base_logline": "A poor boy trades the family cow for magic beans, climbs a beanstalk to a giant's realm, steals treasures, and ultimately kills the giant to secure wealth for his mother",
                "characters": "Jack: Impulsive but clever thief, Giant: Man-eating ogre guarding riches, Jack's Mother: Desperate widow",
                "conflict": "Jack's poverty vs. the giant's hoarded wealth",
                "setting": "Rural cottage → colossal cloud-kingdom above the beanstalk",
                "themes": "Risk vs. reward, social mobility through trickery"
            },
            "sugar_shelter": {
                "original_title": "Hansel & Gretel",
                "genre": "Folk Horror",
                "base_logline": "Two starving children abandon hope when their parents leave them in the woods; they find a candy house owned by a witch who plans to eat them, but they outwit and kill her",
                "characters": "Hansel & Gretel: Resourceful siblings, Witch: Cannibal crone, Parents: Poor, neglectful",
                "conflict": "Children's survival vs. witch's hunger",
                "setting": "Deep forest, edible cottage",
                "themes": "Child abandonment, cunning over cruelty"
            }
        }
        
        # Expansion prompt template based on your examples
        self.expansion_prompt = """
        I want to expand all the components of this story blueprint, so that each line and concept is more detailed and rich. It should be optimal for smart weaving of each blueprint into a full short story. The structure and idea should remain the same, unless there are clear opportunities to make the story better.

        Please create a detailed expansion following this format:

        ### **{story_id}. {title}**

        **Genre:** {genre}

        ---

        #### **Original Story Blueprint: {original_title}**

        * **Genre:** {original_genre}
        * **Logline:** {original_logline}

        **Expanded Essential Ingredients:**

        | Component | Expanded Description |
        |-----------|---------------------|
        | **Character** | {detailed_character_analysis} |
        | **Conflict** | {detailed_conflict_analysis} |
        | **Setting** | {detailed_setting_analysis} |
        | **Theme** | {detailed_theme_analysis} |
        | **Exposition** | {detailed_exposition} |
        | **Inciting Incident** | {detailed_inciting} |
        | **Rising Action** | {detailed_rising} |
        | **Climax** | {detailed_climax} |
        | **Falling Action** | {detailed_falling} |
        | **Resolution** | {detailed_resolution} |

        ---

        #### **New Story Blueprint: {new_title}**

        **One–Sentence Logline:** {new_logline}

        **Detailed Expansion:**

        | Component | Expanded Description |
        |-----------|---------------------|
        | **Character** | {new_detailed_character} |
        | **Conflict** | {new_detailed_conflict} |
        | **Setting** | {new_detailed_setting} |
        | **Theme** | {new_detailed_theme} |
        | **Exposition** | {new_detailed_exposition} |
        | **Inciting Incident** | {new_detailed_inciting} |
        | **Rising Action** | {new_detailed_rising} |
        | **Rising Action** | {new_detailed_rising} |
        | **Climax** | {new_detailed_climax} |
        | **Falling Action** | {new_detailed_falling} |
        | **Resolution** | {new_detailed_resolution} |
        """
        
        print("🎨 Blueprint Generator initialized")
        print(f"📁 Blueprints directory: {self.blueprints_dir}")
    
    def generate_blueprint_from_concept(self, story_concept: str, base_fairy_tale: str = None) -> CompleteBlueprint:
        """
        Generate a detailed blueprint from a simple story concept.
        
        Args:
            story_concept: Basic story idea or title
            base_fairy_tale: Optional fairy tale to base it on
            
        Returns:
            Complete detailed blueprint
        """
        # For now, create a structured blueprint based on your examples
        # In production, this would use an LLM API call
        
        if "huff" in story_concept.lower() or "heal" in story_concept.lower():
            return self._create_huff_heal_blueprint()
        elif "high crimes" in story_concept.lower():
            return self._create_high_crimes_blueprint()
        elif "sugar shelter" in story_concept.lower():
            return self._create_sugar_shelter_blueprint()
        else:
            # Create a generic template that can be filled in
            return self._create_template_blueprint(story_concept)
    
    def _create_huff_heal_blueprint(self) -> CompleteBlueprint:
        """Create the detailed Huff & Heal blueprint"""
        
        original = OriginalStoryBlueprint(
            title="Little Red Riding Hood",
            genre="Folk Horror / Cautionary Tale",
            logline="A young girl encounters a dangerous wolf while traveling to her grandmother's house, learning harsh lessons about trust and the dangers that lurk in seemingly innocent encounters.",
            character="**Little Red Riding Hood:** Innocent, trusting child whose naivety makes her vulnerable to predatory manipulation. **Big Bad Wolf:** Cunning predator representing the dangers that exploit innocence and trust. **Grandmother:** Vulnerable elder symbolizing the fragility of safety and family protection.",
            conflict="Little Red's innocent trust and desire to help her grandmother directly conflicts with the Wolf's predatory intentions, creating a fundamental tension between innocence and malevolence.",
            setting="A seemingly peaceful forest path that transforms from familiar safety to threatening unknown, leading to Grandmother's cottage—a space meant to represent security but becomes a site of vulnerability.",
            theme="Explores stranger danger, the loss of innocence, predator-prey dynamics in society, and the harsh transition from childhood trust to adult wariness.",
            exposition="Little Red Riding Hood is sent by her mother to deliver food to her ailing grandmother, establishing her caring nature and the routine trust of family obligations.",
            inciting="Little Red encounters the Wolf in the forest, who charmingly inquires about her destination, beginning the predatory manipulation that will drive the story's conflict.",
            rising="The Wolf races ahead to Grandmother's house, devours the elderly woman, and disguises himself in her bed, preparing his trap while Little Red continues her innocent journey.",
            climax="Little Red arrives at the cottage and engages in the famous dialogue with the disguised Wolf, her growing suspicion culminating in the revelation of his true identity and immediate threat.",
            falling="The Wolf attempts to devour Little Red, but intervention (traditionally a woodsman) arrives to rescue her and punish the predator.",
            resolution="Little Red survives the encounter, forever changed by the experience, having learned harsh lessons about trust, appearances, and the dangers that exist in the world."
        )
        
        new = NewStoryBlueprint(
            title="Huff & Heal",
            genre="Dark Eco-Comedy / Woodland Noir",
            logline="A misunderstood wolf-therapist must expose a poaching cartel run by Granny without breaking patient confidentiality or triggering a forest-wide relapse.",
            character=DetailedStoryComponent(
                "Character",
                "**Dr. Lupus Grimm:** A reformed Big Bad Wolf who has undergone extensive anger management and therapeutic training, now serving as the forest's first licensed therapist. His transformation from predator to healer creates complex internal tensions—he deeply understands both the predatory mindset and the trauma it causes. His patients include the very creatures his species once terrorized, making every session a delicate balance of professional competence and personal redemption. **Red:** A young courier unknowingly working for her grandmother's illegal operations, representing innocence corrupted by family loyalty. Her character arc involves awakening to moral complexity and choosing between family ties and ethical responsibility. **Granny:** The story's true antagonist, a manipulative elder who exploits both family bonds and community trust to run a sophisticated poaching operation, embodying the corruption of traditional authority figures."
            ),
            conflict=DetailedStoryComponent(
                "Conflict",
                "Dr. Grimm faces an impossible ethical dilemma: his therapeutic oath prevents him from breaking patient confidentiality, yet the information shared in sessions reveals Granny's extensive poaching network that threatens his patients' safety and recovery. The conflict intensifies as his dual identity as both former predator and current protector creates suspicion from both his patients and the authorities. The deeper conflict explores whether redemption is possible when past sins create ongoing obstacles to doing good, and whether breaking sacred professional ethics can be justified to prevent greater harm."
            ),
            setting=DetailedStoryComponent(
                "Setting",
                "The story unfolds in a modern forest preserve where Dr. Grimm has established a therapeutic sanctuary—a repurposed clearing where natural acoustics and calming atmosphere aid in trauma recovery. His office is built into a large hollow tree, symbolizing both shelter and the natural integration of healing. The forest itself is under siege from Granny's sophisticated poaching operation, which uses drones, hidden cameras, and traditional traps, creating a contrast between the ancient woodland and modern exploitation. Granny's cottage serves as the operation's headquarters, its wholesome exterior masking high-tech criminal enterprise."
            ),
            theme=DetailedStoryComponent(
                "Theme",
                "The story explores redemption and the ongoing cost of past actions, examining whether true change is possible when society refuses to forget past transgressions. It delves into professional ethics versus moral imperatives, questioning when breaking sacred oaths becomes necessary for the greater good. Environmental themes address the exploitation of nature by those who present themselves as protectors, while psychological themes explore trauma recovery, the therapist-patient relationship, and the complex dynamics between predator and prey when traditional roles are reversed."
            ),
            exposition=DetailedStoryComponent(
                "Exposition",
                "Dr. Grimm conducts his morning therapy circle with a diverse group of woodland creatures—rabbits who still flinch at his scent, deer with PTSD from hunting experiences, and birds whose migration patterns have been disrupted by human activity. The session demonstrates both his therapeutic competence and the ongoing challenge of earning trust from those his species traditionally terrorized. The forest sanctuary represents years of careful work to create a safe space, but subtle signs suggest this safety is under threat."
            ),
            inciting_incident=DetailedStoryComponent(
                "Inciting Incident",
                "During a private session with a traumatized deer, Dr. Grimm learns that Red has been using forest paths to transport mysterious packages to her grandmother. The deer's description of unusual nighttime activities, combined with missing animals reports, creates the first clear indication that Granny is running illegal operations. This revelation forces Dr. Grimm to confront whether his therapeutic obligations extend to protecting the entire forest community, even if it means violating patient confidentiality."
            ),
            rising_action=DetailedStoryComponent(
                "Rising Action",
                "Dr. Grimm's investigation reveals the scope of Granny's operation—a sophisticated network using Red as an unwitting courier while targeting his therapy patients as valuable exotic animals. His attempts to gather evidence without violating professional ethics become increasingly difficult as more patients report suspicious activities. The tension escalates when Red begins attending his group sessions, creating a conflict between her therapeutic needs and her unknowing participation in the operation threatening his other patients. Granny's awareness of his investigation leads to direct threats against the sanctuary."
            ),
            climax=DetailedStoryComponent(
                "Climax",
                "The climactic confrontation occurs when Granny's poaching team attempts to raid the sanctuary during a large group therapy session. Dr. Grimm must choose between maintaining his therapeutic persona and reverting to his predatory instincts to protect his patients. The scene forces him to use his knowledge of both predator and prey psychology, his therapeutic skills to calm panicked animals, and his wolf instincts to outmaneuver the poachers. Red discovers her grandmother's true nature and must choose between family loyalty and protecting the animals she has unknowingly helped endanger."
            ),
            falling_action=DetailedStoryComponent(
                "Falling Action",
                "The aftermath of the confrontation reveals the full extent of Granny's operation to the authorities, vindicated Dr. Grimm's actions while raising questions about his methods. Red faces the trauma of discovering her grandmother's deception and her own unwitting complicity, requiring therapeutic support from Dr. Grimm despite their complex history. The forest community grapples with the revelation that danger came from within their trusted network, challenging their understanding of safety and community."
            ),
            resolution=DetailedStoryComponent(
                "Resolution",
                "Dr. Grimm establishes new protocols for the sanctuary that balance patient confidentiality with community safety, creating a model for ethical therapeutic practice in complex situations. Red becomes an advocate for forest protection, using her knowledge of Granny's networks to help authorities dismantle similar operations. The story concludes with Dr. Grimm earning deeper trust from his patients—not despite his predatory nature, but because he chose to use those instincts in their defense. The sanctuary expands, representing both personal redemption and community healing, though the work of rebuilding trust continues."
            )
        )
        
        return CompleteBlueprint(
            story_id=1,
            original=original,
            new=new,
            generated_at=datetime.now().isoformat(),
            blueprint_prompt_version="1.0"
        )
    
    def _create_high_crimes_blueprint(self) -> CompleteBlueprint:
        """Create the detailed High Crimes blueprint based on your example"""
        
        original = OriginalStoryBlueprint(
            title="Jack & the Beanstalk",
            genre="Heroic Folk-Tale",
            logline="A poor boy trades the family cow for magic beans, climbs a beanstalk to a giant's realm, steals treasures, and ultimately kills the giant to secure wealth for his mother.",
            character="**Jack:** Impulsive but 'clever' thief whose desperation drives increasingly dangerous decisions. **Giant:** Man-eating ogre guarding immense riches in his cloud-kingdom fortress. **Jack's Mother:** Desperate widow whose poverty motivates Jack's dangerous quest for wealth.",
            conflict="Jack's crushing poverty and desire for social mobility conflicts with the Giant's hoarded wealth and territorial protection, creating a classic David vs. Goliath struggle with moral ambiguity.",
            setting="The story moves from a humble rural cottage representing poverty and limitation to a massive cloud-kingdom above the beanstalk, symbolizing unreachable wealth and power, connected by the magical beanstalk that serves as both opportunity and danger.",
            theme="Explores risk versus reward dynamics, the ethics of theft when motivated by desperation, social mobility through trickery rather than honest work, and the moral complexity of survival in an inequitable system.",
            exposition="Jack's family faces destitution, forcing the desperate decision to sell their only valuable possession—their cow—establishing the economic desperation that drives all subsequent actions.",
            inciting="Jack trades the family cow for mysterious magic beans, a decision that appears foolish but creates the opportunity that will transform their fortunes, for better or worse.",
            rising="The beanstalk grows overnight, providing access to the Giant's realm. Jack's escalating thefts—first gold, then a hen that lays golden eggs, finally a magical harp—increase both the stakes and the danger as the Giant becomes aware of the intrusion.",
            climax="The Giant discovers Jack's theft and pursues him down the beanstalk in a life-or-death chase that will determine whether Jack's gamble pays off or costs him everything.",
            falling="Jack chops down the beanstalk, causing the Giant to fall to his death, eliminating the threat but also destroying the bridge between the two worlds.",
            resolution="Jack and his mother achieve wealth and security through the stolen treasures, living rich and unpunished, raising questions about justice and the morality of survival-driven theft."
        )
        
        new = NewStoryBlueprint(
            title="High Crimes",
            genre="Tragic Fable / Eco-Thriller",
            logline="A gentle cloud-farmer giant must save his starving sky-folk after serial burglar Jack fells the only beanstalk that feeds them.",
            character=DetailedStoryComponent(
                "Character",
                "**Nimbus:** An autistic giant and agricultural savant who serves as the primary food producer for the floating cloud-city of Stratopolis. His neurological differences make him exceptionally gifted at understanding complex ecological systems but also vulnerable to social manipulation and violence. His gentle nature and dedication to feeding his community contrasts sharply with the surface world's perception of giants as monsters. **Jack:** A serial burglar and con artist whose charming exterior masks increasingly desperate criminal behavior. His thefts escalate from personal survival to systematic exploitation, representing the worst aspects of surface-world capitalism and individualism. **The Sky-Folk:** A diverse community of floating-city inhabitants who depend entirely on Nimbus's agricultural expertise for survival, making them vulnerable to surface-world interference."
            ),
            conflict=DetailedStoryComponent(
                "Conflict", 
                "Nimbus faces an impossible choice: continue trying to maintain peaceful relations with the surface world despite Jack's escalating thefts, or take decisive action that could be interpreted as the 'monstrous giant' behavior that surface-dwellers expect. The deeper conflict explores the systematic exploitation of resources and vulnerable populations by those who present themselves as clever heroes. As Jack's thefts threaten the entire cloud-city's food supply, Nimbus must overcome his peaceful nature to protect his community while avoiding confirming surface-world stereotypes about giant violence."
            ),
            setting=DetailedStoryComponent(
                "Setting",
                "**Stratopolis** is an elaborate floating city built on interconnected cloud-platforms, sustained by Nimbus's revolutionary sky-agriculture that uses cloud moisture and high-altitude growing techniques. The city exists in perpetual storms, with the beanstalk serving as the only stable connection to the surface world and the crucial conduit for the magical nutrients that make sky-farming possible. The contrast between the struggling surface world and the abundant but vulnerable sky-city highlights themes of resource distribution and environmental sustainability. Nimbus's terraced gardens float on cloud-platforms, representing harmony between technology and nature that Jack's intrusions threaten to destroy."
            ),
            theme=DetailedStoryComponent(
                "Theme",
                "The story provocatively explores the exploitation of 'others' through ableist stereotypes and assumptions, examining how society fears and exploits those who are different while benefiting from their contributions. Food insecurity serves as both literal threat and metaphor for resource hoarding and distribution inequality. The narrative challenges traditional hero myths by revealing how individual 'cleverness' can mask systematic exploitation and environmental destruction. Deeper themes include the cost of maintaining peaceful communities in a violent world and the moral complexity of protective violence when vulnerable populations are threatened."
            ),
            exposition=DetailedStoryComponent(
                "Exposition",
                "Nimbus tends his revolutionary sky-bean gardens that feed the entire population of Stratopolis, his autistic focus and pattern recognition making him uniquely gifted at understanding the complex ecological relationships that sustain life in the clouds. The city thrives under his care, but their isolation and dependence on a single food source makes them vulnerable to surface-world interference. The beanstalk represents both connection and danger—necessary for trade and nutrients but also providing access for exploitation."
            ),
            inciting_incident=DetailedStoryComponent(
                "Inciting Incident",
                "Jack's first theft of golden seed-pods seems minor but disrupts the delicate ecological balance of the sky-farms. These aren't mere treasures but essential genetic material for crop diversity and food security. Jack's inability to understand or care about the broader implications of his theft sets the stage for escalating environmental and social disaster. Nimbus's attempts to explain the importance of the seeds are dismissed as the ramblings of a simple giant, establishing the ableist assumptions that enable continued exploitation."
            ),
            rising_action=DetailedStoryComponent(
                "Rising Action",
                "Jack returns with increasingly sophisticated tools—culminating in a chainsaw that represents industrial surface-world destruction. His systematic harvesting of the beanstalk threatens the sky-city's food supply and connection to essential nutrients. Nimbus's desperate attempts at communication and negotiation are ignored or misinterpreted as threats. As famine looms in Stratopolis, Nimbus faces pressure from his community to take action while struggling with his peaceful nature and fear of confirming surface-world prejudices about giant violence. The rising tension builds toward a choice between passive victimhood and protective action."
            ),
            climax=DetailedStoryComponent(
                "Climax",
                "In a desperate act of environmental and community defense, Nimbus plunges earthward with his last megabean—a seed containing the genetic material necessary to regrow the entire agricultural system. As he plants it in the earth, the seed rockets upward with devastating force, creating a new beanstalk that skewers Jack mid-trunk. This moment represents Nimbus choosing violent action to protect his community, but also the tragic necessity of destroying the peaceful ideals he cherished. The new stalk's violent birth symbolizes how environmental protection sometimes requires dramatic, disruptive action."
            ),
            falling_action=DetailedStoryComponent(
                "Falling Action",
                "The new hybrid beanstalk bridges the two worlds more permanently, allowing for proper communication and resource sharing between surface and sky communities. Aid convoys begin traveling both directions, with surface dwellers finally understanding the sky-city's needs and contributions. Jack's death serves as a cautionary tale about the consequences of exploitative behavior, while also raising questions about the cost of justice and protection. Nimbus grapples with having taken a life, even in defense of his community."
            ),
            resolution=DetailedStoryComponent(
                "Resolution",
                "A formal trade accord is established between surface and sky worlds, with Nimbus teaching sustainable farming techniques to surface communities struggling with environmental degradation. The new relationship recognizes the sky-city's sovereignty while creating mutual benefit rather than exploitation. Nimbus's role evolves from victim to teacher, using his agricultural expertise to help both worlds achieve food security. The story concludes with the understanding that true heroism lies in creating systems that prevent exploitation rather than simply responding to it, though the memory of necessary violence serves as a sobering reminder of protection's costs."
            )
        )
        
        return CompleteBlueprint(
            story_id=2,
            original=original,
            new=new,
            generated_at=datetime.now().isoformat(),
            blueprint_prompt_version="1.0"
        )
    
    def _create_sugar_shelter_blueprint(self) -> CompleteBlueprint:
        """Create the detailed Sugar Shelter blueprint"""
        
        original = OriginalStoryBlueprint(
            title="Hansel & Gretel",
            genre="Folk Horror",
            logline="Two starving children abandon hope when their parents leave them in the woods; they find a candy house owned by a witch who plans to eat them, but they outwit and kill her.",
            character="**Hansel & Gretel:** Resourceful siblings forced to survive abandonment through cunning and mutual support. **Witch:** Cannibal crone who preys on vulnerable children. **Parents:** Poor, neglectful caregivers who abandon their children in desperation.",
            conflict="The children's desperate need for survival conflicts with the witch's predatory hunger, creating a life-or-death struggle between innocence and malevolence.",
            setting="Deep, threatening forest leading to an enchanted candy cottage that serves as both salvation and trap.",
            theme="Child abandonment, survival through cunning, the triumph of resourcefulness over predatory evil.",
            exposition="Parents plot to abandon their children due to poverty and food scarcity, establishing the desperate circumstances that force the children into danger.",
            inciting="The children become lost in the forest and discover the witch's candy house, beginning their entrapment in a predatory situation.",
            rising="The witch fattens Hansel while enslaving Gretel, building tension toward the climactic confrontation that will determine their survival.",
            climax="Gretel outsmarts the witch and shoves her into the oven, eliminating the threat through clever reversal of the witch's own methods.",
            falling="The children escape with the witch's jewels and treasures, having gained both freedom and wealth through their ordeal.",
            resolution="They return home rich and empowered, having survived abandonment and predation through mutual support and intelligence."
        )
        
        new = NewStoryBlueprint(
            title="Sugar Shelter",
            genre="Psychological Horror / Candy-Goth",
            logline="A retired social worker's edible trauma refuge is misbranded a cannibal den exactly when meth-lord parents come to 'claim' their abandoned kids.",
            character=DetailedStoryComponent(
                "Character",
                "**Greta Müller:** A retired social worker and candy-architect therapist who has dedicated her life to creating healing spaces for abandoned and traumatized children. Her unconventional methods involve using edible environments and sweet-scented pheromones to create calming, nurturing spaces that help children process trauma. Her past includes losing her own children to the system she worked within, driving her to create an alternative sanctuary. **Hansel & Gretel:** Siblings abandoned by drug-addicted parents, representing the vulnerability of children caught in addiction's wake. **The Parents:** Meth-lord parents who return not out of love but to exploit their children for drug trafficking operations, embodying the worst aspects of familial manipulation and exploitation."
            ),
            conflict=DetailedStoryComponent(
                "Conflict",
                "Greta must protect Hansel and Gretel from their returning parents while defending her sanctuary against viral media misrepresentation and militia vigilantes. The deeper conflict explores the intersection of good intentions and public perception, where therapeutic innovation is twisted into predatory narrative. Greta's methods, designed to help children heal from trauma, are weaponized against her by those who would rather perpetuate cycles of abuse than confront systemic failures in child protection."
            ),
            setting=DetailedStoryComponent(
                "Setting",
                "**Syrup Swamp** is a biotech sugar forest where Greta has constructed therapeutic environments using edible architecture and calming pheromone-infused candy walls. The setting combines cutting-edge trauma therapy with whimsical candy-land aesthetics, creating spaces that help children feel safe while processing difficult experiences. The swamp's remote location provides isolation for healing but also makes it vulnerable to misinterpretation and attack. The contrast between the healing intent and the media's 'gingerbread house' narrative creates dramatic irony throughout the story."
            ),
            theme=DetailedStoryComponent(
                "Theme",
                "The story examines media sensationalism and how innovative approaches to social problems can be twisted into moral panic narratives. It explores the concept of found family versus biological family, questioning whether blood relations automatically confer parental rights regardless of behavior. Addiction fallout and its impact on children serves as a backdrop for examining how society fails to protect its most vulnerable members while punishing those who try to help. The theme of therapeutic innovation versus traditional methods highlights the resistance to change in systems meant to help children."
            ),
            exposition=DetailedStoryComponent(
                "Exposition",
                "Greta has spent years perfecting her pheromone-calming candy walls and edible therapy environments, creating a sanctuary where traumatized children can heal through innovative sensory experiences. Her methods combine traditional therapy with biochemical comfort, using sugar and scent to create neurological calm. The facility serves multiple abandoned children, with Hansel and Gretel being her newest residents who are just beginning to trust and heal from their abandonment trauma."
            ),
            inciting_incident=DetailedStoryComponent(
                "Inciting Incident",
                "Aerial drone footage of the candy facility is leaked online, with viral social media posts misidentifying it as a 'witch's house' and spreading conspiracy theories about child endangerment. The footage, taken out of context, transforms therapeutic innovation into sinister narrative, triggering moral panic and attracting dangerous attention from vigilante groups and the children's original parents who see an opportunity for exploitation."
            ),
            rising_action=DetailedStoryComponent(
                "Rising Action",
                "'Child-eater' headlines spark militia raids and protests outside the facility, while Hansel and Gretel's meth-lord parents return claiming parental rights—not out of love but to exploit the children for drug trafficking operations. Greta must simultaneously defend her methods to authorities, protect the children from media attention, and prepare for confrontation with both vigilantes and the returning parents. The tension builds as multiple threat levels converge on the sanctuary."
            ),
            climax=DetailedStoryComponent(
                "Climax",
                "When the parents and militia attempt to breach the facility simultaneously, Greta makes the desperate decision to liquify the candy walls, trapping the invading parents in protective syrup while creating barriers against the militia. This dramatic action saves the children but also appears to confirm the viral 'witch' narrative, creating a complex moral victory that comes at the cost of public understanding. The syrup trap becomes both protection and public relations disaster."
            ),
            falling_action=DetailedStoryComponent(
                "Falling Action",
                "SWAT teams arrive to find a gooey standoff with parents trapped in syrup and Greta protecting terrified children. The investigation that follows reveals the parents' criminal history and Greta's legitimate therapeutic credentials, but the viral nature of the initial story makes public rehabilitation difficult. The media circus continues even as authorities clear Greta of wrongdoing, highlighting how truth often cannot compete with sensational narrative."
            ),
            resolution=DetailedStoryComponent(
                "Resolution",
                "The parents are jailed for drug trafficking and child endangerment, while Greta is officially cleared and her methods validated by child psychology experts. However, she remains forever meme-ified as the 'candy witch,' making her work more difficult despite its effectiveness. Hansel and Gretel find permanent safe placement, but Greta's story serves as a cautionary tale about innovation in child welfare and the power of viral misinformation to destroy well-intentioned work. The resolution is bittersweet—justice served but reputation permanently damaged."
            )
        )
        
        return CompleteBlueprint(
            story_id=3,
            original=original,
            new=new,
            generated_at=datetime.now().isoformat(),
            blueprint_prompt_version="1.0"
        )
    
    def _create_template_blueprint(self, story_concept: str) -> CompleteBlueprint:
        """Create a template blueprint for custom concepts"""
        
        # This would be replaced with LLM generation in production
        original = OriginalStoryBlueprint(
            title="Custom Fairy Tale",
            genre="Folk Tale",
            logline="A classic tale waiting to be reimagined.",
            character="Traditional characters with archetypal roles",
            conflict="Classic conflict between good and evil",
            setting="Traditional fairy tale setting",
            theme="Universal themes of growth and triumph",
            exposition="Traditional opening",
            inciting="Traditional inciting incident",
            rising="Traditional rising action",
            climax="Traditional climax",
            falling="Traditional falling action",
            resolution="Traditional resolution"
        )
        
        new = NewStoryBlueprint(
            title=story_concept,
            genre="Contemporary Reimagining",
            logline="A modern twist on a classic tale.",
            character=DetailedStoryComponent("Character", "Characters reimagined for contemporary context"),
            conflict=DetailedStoryComponent("Conflict", "Contemporary conflict with modern stakes"),
            setting=DetailedStoryComponent("Setting", "Modern setting with rich detail"),
            theme=DetailedStoryComponent("Theme", "Contemporary themes and social commentary"),
            exposition=DetailedStoryComponent("Exposition", "Modern opening establishing the world"),
            inciting_incident=DetailedStoryComponent("Inciting Incident", "Contemporary inciting event"),
            rising_action=DetailedStoryComponent("Rising Action", "Modern escalation of stakes"),
            climax=DetailedStoryComponent("Climax", "Contemporary climactic confrontation"),
            falling_action=DetailedStoryComponent("Falling Action", "Modern consequences"),
            resolution=DetailedStoryComponent("Resolution", "Contemporary resolution")
        )
        
        return CompleteBlueprint(
            story_id=999,
            original=original,
            new=new,
            generated_at=datetime.now().isoformat(),
            blueprint_prompt_version="1.0"
        )
    
    def save_blueprint(self, blueprint: CompleteBlueprint) -> str:
        """Save blueprint to JSON file"""
        filename = f"blueprint_{blueprint.story_id:02d}_{blueprint.new.title.lower().replace(' ', '_').replace('&', 'and')}.json"
        filepath = self.blueprints_dir / filename
        
        # Convert to dict for JSON serialization
        blueprint_dict = asdict(blueprint)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blueprint_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Blueprint saved: {filepath}")
        return str(filepath)
    
    def export_to_flipside_format(self, blueprint: CompleteBlueprint) -> str:
        """Export blueprint in format compatible with existing Flipside processor"""
        
        # Create the format expected by the existing system
        flipside_format = f"""{blueprint.story_id} {blueprint.new.title} — {blueprint.new.genre}

Logline: {blueprint.new.logline}

| Character | {blueprint.new.character.expanded_description[:200]}... |
| Conflict  | {blueprint.new.conflict.expanded_description[:200]}... |
| Setting   | {blueprint.new.setting.expanded_description[:200]}... |
| Theme     | {blueprint.new.theme.expanded_description[:200]}... |

Arc
    1.    Exposition: {blueprint.new.exposition.expanded_description[:300]}...
    2.    Inciting: {blueprint.new.inciting_incident.expanded_description[:300]}...
    3.    Rising: {blueprint.new.rising_action.expanded_description[:300]}...
    4.    Climax: {blueprint.new.climax.expanded_description[:300]}...
    5.    Falling: {blueprint.new.falling_action.expanded_description[:300]}...
    6.    Resolution: {blueprint.new.resolution.expanded_description[:300]}..."""
        
        return flipside_format
    
    def generate_all_fairer_tales_blueprints(self) -> List[CompleteBlueprint]:
        """Generate blueprints for all 11 Fairer Tales stories"""
        
        story_concepts = [
            "Huff & Heal", "Blowback", "Cinder-Debt", "Hairloom", "High Crimes",
            "Just-Right Trap", "Mirror Error", "Never Grown", "Spin Cycle", 
            "Stockholm", "Sugar Shelter"
        ]
        
        blueprints = []
        for concept in story_concepts:
            print(f"🎨 Generating blueprint for: {concept}")
            blueprint = self.generate_blueprint_from_concept(concept)
            filepath = self.save_blueprint(blueprint)
            blueprints.append(blueprint)
            
        print(f"✅ Generated {len(blueprints)} Fairer Tales blueprints")
        return blueprints

# Test the generator
if __name__ == "__main__":
    generator = BlueprintGenerator()
    
    # Test with Huff & Heal
    blueprint = generator.generate_blueprint_from_concept("Huff & Heal")
    filepath = generator.save_blueprint(blueprint)
    
    # Export to Flipside format
    flipside_format = generator.export_to_flipside_format(blueprint)
    print(f"\n📋 Flipside Format:\n{flipside_format}")
    
    print(f"\n✅ Blueprint generation test complete!")
    print(f"💾 Saved to: {filepath}")