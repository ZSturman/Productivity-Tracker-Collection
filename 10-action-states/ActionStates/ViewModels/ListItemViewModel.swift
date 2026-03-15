//
//  ListItemViewModel.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
//

import CoreData
import Foundation

class ListItemViewModel: ObservableObject {
    let container: NSPersistentContainer
    @Published var listItems = [ListItemEntity]()

    init(container: NSPersistentContainer) {
        self.container = container
    }

    func fetchListItems(for list: ListEntity) {
        listItems = list.listItems?.allObjects as? [ListItemEntity] ?? []
    }
    
    func addListItem(listItem: String, to list: ListEntity) {
        let newListItem = ListItemEntity(context: container.viewContext)
        newListItem.name = listItem
        newListItem.list = list
        list.addToListItems(newListItem)
        saveListItems(list: list)
    }
    
    func saveListItems(list: ListEntity) {
        do {
            try container.viewContext.save()
            fetchListItems(for: list)
        } catch let error {
            print("Error saving list items. \(error)")
        }
    }
}
