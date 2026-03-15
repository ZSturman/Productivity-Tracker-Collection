//
//  TopicListViewModel.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/23/23.
//

import CoreData
import Foundation

class TopicViewModel: ObservableObject {
    @Published var topics: [TopicEntity] = []
    
    @Published var topicName = ""
    @Published var topicDescription = ""
    
    private var moc: NSManagedObjectContext
    
    init(moc: NSManagedObjectContext) {
        self.moc = moc
        fetchTopics()
        if topics.isEmpty {
            if UserDefaults.standard.bool(forKey: "HasLaunchedBefore") == false {
                createDefaultTopics()
                UserDefaults.standard.set(true, forKey: "HasLaunchedBefore")
            }
        }
    }
    
    func fetchTopics() {
        let fetchRequest: NSFetchRequest<TopicEntity> = TopicEntity.fetchRequest()
        do {
            self.topics = try moc.fetch(fetchRequest)
        } catch {
            print("Failed to fetch topics: \(error.localizedDescription)")
        }
    }
    
    func addNewTopic() {
        let newTopic = TopicEntity(context: moc)
        newTopic.id = UUID()
        newTopic.name = topicName
        newTopic.topicDescription = topicDescription
        
        try? moc.save()
    }
    
    func deleteTopic(at offsets: IndexSet) {
        for offset in offsets {
            let topic = topics[offset]
            moc.delete(topic)
        }
        try? moc.save()
    }
    
    
    
    
    func createDefaultTopics() {
        guard let url = Bundle.main.url(forResource: "DefaultTopics", withExtension: "plist"),
              let data = try? Data(contentsOf: url),
              let plist = try? PropertyListSerialization.propertyList(from: data, options: [], format: nil),
              let defaultTopics = plist as? [[String: String]] else { return }
        
        for topic in defaultTopics {
            let topicEntity = TopicEntity(context: moc)
            topicEntity.id = UUID()
            topicEntity.name = topic["name"]
            topicEntity.topicDescription = topic["description"]
            
            do {
                try moc.save()
            } catch {
                let nsError = error as NSError
                print("Unresolved error \(nsError), \(nsError.userInfo)")
            }
        }
        
        fetchTopics()
    }

}
