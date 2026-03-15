//
//  TempTrigger.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import CoreData
import SwiftUI

struct TempTrigger {
    var id: UUID
    // ADD EDITABLE DISPLAY NAME
    var title: String
    var triggerSystemImage: String
    var triggerType: TriggerTypeOptions
    var firstInputID: UUID?
    var lastInputID: UUID?
    var inputs: [TempInput]
    var executions: [TempExecution]
    
    var getLocation: Bool = false
    
    var triggerOutputDate: String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateStyle = .medium
        dateFormatter.timeStyle = .medium
        return dateFormatter.string(from: Date())
    }
    
    var triggerOutputLocation: String? {
        return "Denver, CO"
    }
    
    var triggerOutput: String? {
        return inputs.last?.inputType.inputDescription
    }

    init(id: UUID = UUID(),
         title: String = "New Trigger",
         firstInputID: UUID? = nil,
         lastInputID: UUID? = nil,
         inputs: [TempInput] = [],
         executions: [TempExecution] = []) {
        self.id = id
        self.title = title
        self.triggerType = TriggerTypeOptions(rawValue: title) ?? .buttonMain
        self.triggerSystemImage = triggerType.triggerSystemImageName
        self.firstInputID = firstInputID
        self.lastInputID = lastInputID
        self.inputs = inputs
        self.executions = executions
    }
}


enum TriggerTypeOptions: String, CaseIterable {
    case buttonMain = "Primary button"
    case buttonOne = "Button one"
    case buttonTwo = "Button two"
    case swipeLeft = "Swipe left"
    case swipeLeftButton = "Swipe left button"
    case swipeRight = "Swipe right"
    case swipeRightButton = "Swipe right button"
    
    var triggerTypeName: String {
        return self.rawValue
    }
    
    var triggerSystemImageName: String {
        switch self {
        case .buttonMain:
            return "circle"
        case .buttonOne:
            return "figure.wave.circle.fill"
        case .buttonTwo:
            return "peacesign"
        case .swipeLeft:
            return "arrow.left"
        case .swipeLeftButton:
            return "arrowshape.turn.up.left.circle"
        case .swipeRight:
            return "arrow.right"
        case .swipeRightButton:
            return "arrowshape.turn.up.right.circle"
        }
    }
}

extension TempTrigger {
    init(from trigger: Trigger, in context: NSManagedObjectContext) {
        self.id = trigger.id ?? UUID() // Provide a default value
        self.title = trigger.title ?? "" // Provide a default value
        self.triggerSystemImage = trigger.triggerSystemImage ?? "" // Provide a default value
        self.triggerType = TriggerTypeOptions(rawValue: trigger.triggerType ?? "") ?? .buttonMain // Provide a default value
        
        self.inputs = (trigger.inputs as? Set<Input>).map { $0.map { TempInput(from: $0) } } ?? []
        self.executions = (trigger.executions as? Set<Execution>).map { $0.map { TempExecution(from: $0, in: context) } } ?? []
    }
}





extension Trigger {
    
    convenience init(from tempObject: TempTrigger, in context: NSManagedObjectContext) {
        let entity = NSEntityDescription.entity(forEntityName: "Trigger", in: context)!
        self.init(entity: entity, insertInto: context)
        
        // Set properties using values from the temporary object
        self.id = tempObject.id
        self.title = tempObject.title
        self.triggerSystemImage = tempObject.triggerSystemImage
        self.triggerType = tempObject.triggerType.rawValue
        self.firstInputID = tempObject.firstInputID
        self.lastInputID = tempObject.lastInputID
        //self.getLocation = tempObject.getLocation
        
        self.addToInputs(NSSet(array: tempObject.inputs.map { Input(from: $0, in: context) }))
        let executionSet = NSSet(array: tempObject.executions.map { Execution(from: $0, in: context) })
        self.addToExecutions(executionSet)
    }
}
