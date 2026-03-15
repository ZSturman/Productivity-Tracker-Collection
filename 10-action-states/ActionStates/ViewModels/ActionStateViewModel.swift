//
//  ActionStateViewModel.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/22/23.
//

import CoreData
import Foundation

class ActionStateViewModel: ObservableObject {
    @Published var manualInput: ManualInputEntity?
    @Published var topic: TopicEntity?
    @Published var type = "Action"
    @Published var name = ""
    @Published var explanation = ""
    @Published var collectLocation = true
    @Published var collectDate = true
    @Published var collectTime = true
    @Published var isShowingManualInputForm = false
    @Published var isManualInputButtonPressed = false
    @Published var actionStates: [ActionStateEntity] = []

    let types = ["Action", "State"]
    
    private var moc: NSManagedObjectContext

    init(moc: NSManagedObjectContext) {
        self.moc = moc
        fetchActionStates()
    }
    
    private func fetchActionStates() {
        let fetchRequest: NSFetchRequest<ActionStateEntity> = ActionStateEntity.fetchRequest()
        
        do {
            actionStates = try moc.fetch(fetchRequest)
        } catch {
            print("Failed to fetch ActionStateEntity: \(error)")
        }
    }
    

    func addNewItem() {
        let newActionState = ActionStateEntity(context: moc)
        newActionState.id = UUID()
        newActionState.name = name
        newActionState.type = type
        newActionState.timestamp = Date()
        newActionState.collectDate = collectDate
        newActionState.collectTime = collectTime
        newActionState.collectLocation = collectLocation
        newActionState.explanation = explanation
        
        if let manualInput = manualInput {
            newActionState.manualInputs = NSSet(array: [manualInput])
        }
        
        if let topic = topic {
            newActionState.topic = NSSet(array: [topic])
        }

        do {
            try moc.save()
        } catch {
            let nsError = error as NSError
            print("Unresolved error \(nsError), \(nsError.userInfo)")
        }
    }
    
}
