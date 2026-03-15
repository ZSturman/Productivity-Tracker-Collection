//
//  FieldViewModel.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import CoreData
import Foundation




class FieldViewModel: ObservableObject {
    let managedObjectContext: NSManagedObjectContext

    @Published var fieldName: String = ""
    @Published var fieldType: String = ""
    @Published var prompt: String = ""
    @Published var order: Int16 = 0
    @Published var fieldVariables: [FieldVariable] = []

    init(context: NSManagedObjectContext) {
        self.managedObjectContext = context
    }

    func createField(from field: InputFieldVariables, order: Int16) -> FieldEntity?  {
        let mirror = Mirror(reflecting: field)
        for child in mirror.children {
            if let propertyName = child.label {
                print("Property: \(propertyName), Value: \(child.value)")
            }
        }
        print("------")
        
        guard !field.commonAttributes.name.isEmpty else {
            return nil
        }
        
        let fieldEntity = FieldEntity(context: managedObjectContext)
        fieldEntity.id = UUID()
        fieldEntity.fieldName = field.commonAttributes.name
        fieldEntity.fieldType = field.commonAttributes.selection
        fieldEntity.prompt = field.commonAttributes.prompt
        fieldEntity.order = order
        
        var fieldVariablesInstance: FieldVariables?
        
        switch field.commonAttributes.selection {
        case "Text":
            fieldVariablesInstance = field.textFieldAttributes
        case "Count":
            fieldVariablesInstance = field.countFieldAttributes
        case "Bool":
            fieldVariablesInstance = field.boolFieldAttributes
        case "Number":
            fieldVariablesInstance = field.numberFieldAttributes
        case "Choose from list":
            fieldVariablesInstance = field.listFieldAttributes
        default:
            // Handle other cases as necessary
            break
        }
        
        if let fieldVariablesInstance = fieldVariablesInstance {
            self.fieldVariables = fieldVariablesInstance.getVariables()
        }
        
        
        
        
        
        
//        if field.selection == "Text" {
//            let textFieldVariables = TextFieldVariables(selection: field.selection,
//                                                        textDefaultBool: field.textDefaultBool,
//                                                        textDefault: field.textDefault)
//            self.fieldVariables = textFieldVariables.getVariables()
//        }
//
//        if field.selection == "Count" {
//            let countFieldVariables = CountFieldVariables(selection: field.selection,
//                                                          countDirection: field.countDirection,
//                                                          countDecimals: field.countDecimals,
//                                                          countNegatives: field.countNegatives,
//                                                          countCurrency: field.countCurrency,
//                                                          countTo: field.countTo,
//                                                          countToValue: field.countToValue,
//                                                          countToResult: field.countToResult,
//                                                          countToAlertBool: field.countToAlertBool,
//                                                          countFrom: field.countFrom,
//                                                          countFromValue: field.countFromValue,
//                                                          stepCountValue: field.stepCountValue)
//            self.fieldVariables = countFieldVariables.getVariables()
//        }
//
//        if field.selection == "Bool" {
//            let boolFieldVariables = BoolFieldVariables(selection: field.selection,
//                                                        boolDefault: field.boolDefault)
//            self.fieldVariables = boolFieldVariables.getVariables()
//        }
//
//        if field.selection == "Number" {
//            let numberFieldVariables = NumberFieldVariables(selection: field.selection,
//                                                            numberDecimals: field.numberDecimals,
//                                                            numberNegative: field.numberNegative,
//                                                            numberCurrency: field.numberCurrency,
//                                                            numberDefault: field.numberDefault
//            )
//
//            self.fieldVariables = numberFieldVariables.getVariables()
//        }
        
//        if field.selection == "Choose from list" {
//            let listFieldVariables = ListFieldVariables(selection: field.selection,
//                                                        listSelectMultiple: field.listSelectMultiple,
//                                                        listAddAtExecution: field.listAddAtExecution
//            )
//            self.fieldVariables = listFieldVariables.getVariables()
//            
//            if let listId = field.listSelectedList {
//                let fetchRequest: NSFetchRequest<ListEntity> = ListEntity.fetchRequest()
//                fetchRequest.predicate = NSPredicate(format: "id == %@", listId as CVarArg)
//                
//                do {
//                    let selectedListEntities = try self.managedObjectContext.fetch(fetchRequest)
//                    if let selectedListEntity = selectedListEntities.first {
//                        fieldEntity.list = selectedListEntity
//                    }
//                } catch {
//                    print("Failed to fetch ListEntity with id \(listId): \(error)")
//                }
//                
//            }
//        }


        // Create FieldVariableEntity for each FieldVariable in self.fieldVariables
        if !self.fieldVariables.isEmpty {
            for fieldVariable in self.fieldVariables {
                let fieldVariableEntity = FieldVariableEntity(context: managedObjectContext)
                fieldVariableEntity.id = UUID()
                fieldVariableEntity.variable = fieldVariable.variable
                fieldVariableEntity.value = fieldVariable.value

                fieldEntity.addToFieldVars(fieldVariableEntity)
            }
        }

        return fieldEntity
    }
}
 
