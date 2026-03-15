//
//  ListsViewModel.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
//

import Foundation
import CoreData

class ListsViewModel: ObservableObject {
    let container: NSPersistentContainer
    @Published var lists = [ListEntity]()

    init(container: NSPersistentContainer) {
        self.container = container
        loadLists()
    }

    func loadLists() {
        let fetchRequest: NSFetchRequest<ListEntity> = ListEntity.fetchRequest()

        do {
            self.lists = try container.viewContext.fetch(fetchRequest)
        } catch {
            print("Failed to fetch tags: \(error)")
        }
    }
    
    func addList(listName: String) {
        let newList = ListEntity(context: container.viewContext)
        newList.name = listName
        saveList()
    }
    
    func saveList() {
        do {
            try container.viewContext.save()
            loadLists()
        } catch let error {
            print("Error saving list. \(error)")
        }
    }
}
