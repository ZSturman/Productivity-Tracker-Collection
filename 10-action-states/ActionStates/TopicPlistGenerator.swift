//
//  TopicPlistGenerator.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/23/23.
//
import Foundation

struct Topic: Codable {
    var name: String
    var description: String
}

class TopicPlistGenerator {
    
    static func generatePlist() {
        let topics: [Topic] = [
            Topic(name: "Physical Well-being", description: "This includes the desire for health, fitness, vitality, and the absence of pain or discomfort. It's about maintaining the health and functionality of our physical bodies."),
            Topic(name: "Safety and Security", description: "The need for safety and stability in our daily lives, including financial security, health security, and physical safety."),
            Topic(name: "Autonomy", description: "The desire for independence and control over our lives, the ability to make choices and decisions for ourselves."),
            Topic(name: "Competence", description: "We have a deep-rooted desire to be effective in our interactions with the environment. This can also include the need for mastery and understanding in various fields or activities."),
            Topic(name: "Purpose and Meaning", description: "This refers to the desire for life to have a sense of purpose, direction, and personal significance."),
            Topic(name: "Love and Connection", description: "The desire for deep, fulfilling relationships with others. This includes romantic relationships, friendships, and strong family bonds."),
            Topic(name: "Esteem", description: "The need for respect, recognition, and appreciation from others. This also includes self-esteem, or the need for self-respect and self-confidence."),
            Topic(name: "Growth and Learning", description: "The desire for personal development, learning new skills, and acquiring knowledge."),
            Topic(name: "Self-Expression", description: "The need to express our personal ideas, feelings, and identity."),
            Topic(name: "Creativity", description: "The desire to create, to bring something new into existence, to innovate."),
            Topic(name: "Contribution", description: "The desire to contribute to others, to make a positive impact on the world or the people around us."),
            Topic(name: "Transcendence/Spirituality", description: "The desire for spiritual growth, transcendence, and connection to something greater than oneself. This might also include the need for peace and harmony in life."),
            Topic(name: "Adventure and Exploration", description: "The desire to discover new places, experience new things, and break away from routine."),
            Topic(name: "Achievement", description: "The motivation to accomplish challenging goals, overcome obstacles, and rise to the top in one's field."),
            Topic(name: "Fun and Enjoyment", description: "The need for amusement, play, and relaxation. This can be a powerful motivator and adds pleasure to life."),
            Topic(name: "Recognition", description: "The desire to be seen, acknowledged, and valued for our accomplishments, talents, or personal qualities."),
            Topic(name: "Influence", description: "The desire to affect others, shape opinions or events, and have a say in the world around us."),
            Topic(name: "Order", description: "The desire for structure, routine, predictability, and control in one's life."),
            Topic(name: "Beauty and Aesthetics", description: "The desire to appreciate, create, or surround oneself with beauty, be it in physical environments, art, music, or personal appearance."),
            Topic(name: "Curiosity", description: "The need to understand, learn, and make sense of the world around us."),
            Topic(name: "Novelty", description: "The desire for new experiences, variety, and change."),
            Topic(name: "Legacy", description: "The desire to leave something behind, whether it's through one's work, children, or contributions to society."),
            Topic(name: "Authenticity", description: "The desire to be true to oneself, to live in accordance with one's values and beliefs."),
            Topic(name: "Integrity", description: "The desire to be honest, consistent, and to behave in accordance with one's principles."),
            Topic(name: "Resilience", description: "The desire to overcome adversity, to be strong in the face of challenges."),
            Topic(name: "Harmony", description: "The desire for peace, balance, and cooperation in one's relationships and environment."),
            Topic(name: "Generosity", description: "The desire to give, to share, to be kind and helpful to others."),
            Topic(name: "Wisdom", description: "The desire to gain insight, understanding, and a deeper perspective on life."),
            Topic(name: "Simplicity", description: "The desire for a less complicated, more straightforward life. This could involve reducing physical clutter, simplifying relationships, or seeking clarity in one's goals and values."),
            Topic(name: "Courage", description: "The desire to face fear, take risks, and be brave. This could involve stepping out of one's comfort zone, standing up for what one believes in, or facing adversity with strength."),
            Topic(name: "Humility", description: "The desire to be modest and unassuming, recognizing that there is always more to learn and other perspectives to consider."),
            Topic(name: "Equality", description: "The desire for fairness, justice, and equal opportunity. This could manifest as a passion for social justice, a commitment to treating others fairly, or a focus on creating a more equitable society."),
            Topic(name: "Loyalty", description: "The desire to be faithful and dependable. This could involve standing by friends and family, staying true to one's commitments, or maintaining allegiance to a cause or organization."),
            Topic(name: "Compassion", description: "The desire to empathize with the suffering of others and to help alleviate it. This could involve volunteer work, charitable giving, or simply being there for a friend in need."),
            Topic(name: "Respect", description: "The desire to be respected by others, and to show respect for others. This involves recognizing and valuing the worth of all individuals."),
            Topic(name: "Patience", description: "The desire to accept or tolerate delay, problems, or suffering without becoming annoyed or anxious."),
            Topic(name: "Belonging", description: "The desire to be part of a community, to feel connected, and to fit in."),
            Topic(name: "Sustainability", description: "The desire to live in a way that is environmentally responsible and sustainable for future generations."),
            Topic(name: "Reputation", description: "The desire to be regarded in a positive light by others, based on one's actions, accomplishments, or character."),
            Topic(name: "Gratitude", description: "The desire to feel and express appreciation for the good in one's life."),
            Topic(name: "Empowerment", description: "The desire to feel confident and strong, to have control over one's life, and to be able to achieve one's goals."),
            Topic(name: "Nurturing", description: "The desire to care for and protect others, helping them to grow and thrive."),
            Topic(name: "Joy", description: "The desire to experience delight and happiness, and to spread these feelings to others.")
        ]

        let encoder = PropertyListEncoder()
        encoder.outputFormat = .xml

        do {
            let data = try encoder.encode(topics)
            let url = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!.appendingPathComponent("topics.plist")
            try data.write(to: url)
            print("Topics plist file generated at \(url)")
        } catch {
            print("Error encoding topics: \(error)")
        }
    }
}
