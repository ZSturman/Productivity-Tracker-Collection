//
//  TagsViewModel.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
//

import Foundation
import CoreData

class TagsViewModel: ObservableObject {
    let container: NSPersistentContainer
    @Published var tags = [TagEntity]()

    init(container: NSPersistentContainer) {
        self.container = container
        loadTags()
    }

    func loadTags() {
        let fetchRequest: NSFetchRequest<TagEntity> = TagEntity.fetchRequest()

        do {
            self.tags = try container.viewContext.fetch(fetchRequest)
        } catch {
            print("Failed to fetch tags: \(error)")
        }
    }
}
