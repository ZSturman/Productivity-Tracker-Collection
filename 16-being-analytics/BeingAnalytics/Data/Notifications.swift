//
//  Notifications.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/3/23.
//

import Foundation

extension Notification.Name {
    static let newActionStateSaved = Notification.Name("newActionStateSaved")
    
    static let actionStateUpdated = Notification.Name("actionStateUpdated")
    
    static let newExecutionSaved = Notification.Name("newExecutionSaved")
    
    static let deletedActionState = Notification.Name("deletedActionState")
}
